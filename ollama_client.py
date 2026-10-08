import requests
import json


class OllamaClient:

    def __init__(self, url, model):
        self.url = url
        self.model = model

    def chat(self, messages):
        response = requests.post(
            f"{self.url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": True
            },
            stream=True
        )

        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                yield data["message"]["content"]  #yield let's each word be provided to the program one by one instead of all at once

    def summarize(self, messages):

        summary_prompt = [
            {
                "role": "system",
                "content": "Summarize the conversation concisely. Keep important facts, preferences, goals, and context that would help an AI assistant continue the conversation."
            },
            {
                "role": "user",
                "content": str(messages)
            }
        ]

        response = requests.post(
            f"{self.url}/api/chat",
            json={
                "model": self.model,
                "messages": summary_prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]

    def extract_memory(self, messages):

        memory_prompt = [
            {
                "role": "system",
                "content": """
                You are a fact extraction system.

                Extract personal facts explicitly stated by the user.

                Look for:
                - name
                - age
                - field of study or work
                - programming languages being learned
                - long-term goals
                - stable preferences

                IMPORTANT RULES:
                1. Extract every relevant fact stated by the user.
                2. Do not invent or guess information.
                3. Use "name" for the user's name.
                4. Use "age" for the user's age, as a number.
                5. Use "field" for their field of study or work.
                6. Use "learning" for skills or subjects they are learning.
                7. Return ONLY a valid JSON object.
                8. Use an empty JSON object {} if no useful facts are present.
                9. Do not include explanations or markdown.

                Example input:
                "My name is Alex, I am 21 years old, and I study Computer Science."

                Example output:
                {"name": "Alex", "age": 21, "field": "Computer Science"}
                """
            },
            {
                "role": "user",
                "content": json.dumps(messages, ensure_ascii=False)
            }
        ]

        response = requests.post(
            f"{self.url}/api/chat",
            json={
                "model": self.model,
                "messages": memory_prompt,
                "stream": False,
                "options": {
                    "temperature": 0
                }
            }
        )

        response.raise_for_status()

        data = response.json()

        result = data["message"]["content"]
        return result