from storage import ConversationStorage
from memory import Memory
import json

MAX_MESSAGES = 10

class Chatbot:

    def __init__(self, client, storage, memory, system_prompt):
        self.client = client
        self.storage = storage
        self.memory = memory
        self.system_prompt = system_prompt

        self.messages = self.storage.load()

        if not self.messages:
            self.messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            ]

    def ask(self, question):

        self.messages.append({
        "role": "user",
        "content": question
        })

        if len(self.messages) > MAX_MESSAGES:
            self.summarize_old_messages()

        self.update_memory([
        {
            "role": "user",
            "content": question
        }
        ])

        memory_context = ""

        if self.memory.data:
            memory_context = (
                "Known facts about the user:\n"
                + json.dumps(self.memory.data, indent=4)
            )

        messages_for_ai = self.messages.copy()

        if memory_context:
            messages_for_ai.insert(
                1,
                {
                    "role": "system",
                    "content": memory_context
                }
            )

        answer = ""

        for content in self.client.chat(messages_for_ai):
            answer += content
            yield content

        self.messages.append({
            "role": "assistant",
            "content": answer
        })

        self.storage.save(self.messages)

    def clear_history(self):
        self.messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]
        self.storage.save(self.messages)

    def get_stats(self):

        total_characters = sum(
            len(message["content"])
            for message in self.messages
        )

        estimated_tokens = total_characters // 4

        return {
            "messages": len(self.messages),
            "characters": total_characters,
            "estimated_tokens": estimated_tokens
        }

    def summarize_old_messages(self):

        old_messages = self.messages[1:-6]  #Start at index 1 and stop 6 positions from the end

        if not old_messages:
          return

        summary = self.client.summarize(old_messages)

        recent_messages = self.messages[-6:]

        self.messages = [
            self.messages[0],
            {
            "role": "system",
            "content": f"Conversation summary: {summary}"
             }
        ] + recent_messages

        self.storage.save(self.messages)

    def update_memory(self, messages):

        result = self.client.extract_memory(messages)

        extracted = None
        decoder = json.JSONDecoder()

        for index, character in enumerate(result):
            if character == "{":
                try:
                    candidate, _ = decoder.raw_decode(result[index:])

                    if isinstance(candidate, dict):
                        extracted = candidate
                        break

                except json.JSONDecodeError:
                    continue

        if extracted is None:
            return

        if not extracted:
            return

        for key, value in extracted.items():
            if value is None or value == "":
                continue

            existing_value = self.memory.get(key)

            if key == "field" and existing_value is not None:
                if not isinstance(existing_value, list):
                    existing_value = [existing_value]

                if not isinstance(value, list):
                    value = [value]

                for item in value:
                    if item not in existing_value:
                        existing_value.append(item)

                value = existing_value

            elif isinstance(value, list):
                if isinstance(existing_value, list):
                    for item in value:
                        if item not in existing_value:
                            existing_value.append(item)

                    value = existing_value

                elif existing_value is not None:
                    value = [existing_value] + [
                        item for item in value
                        if item != existing_value
                    ]

            self.memory.set(key, value)