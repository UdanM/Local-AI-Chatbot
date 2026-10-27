from config import ollama_url, ollama_model, system_prompt,embedding_model
from ollama_client import OllamaClient
from chatbot import Chatbot
from storage import ConversationStorage
from memory import Memory
from pathlib import Path
from embeddings import EmbeddingClient
from vector_store import VectorStore
import requests
import json

client = OllamaClient(ollama_url, ollama_model)
storage = ConversationStorage("conversation.json")
memory = Memory("memory.json")

vector_store = VectorStore()

embedding_client = EmbeddingClient(
    url=ollama_url,
    model=embedding_model
)

chatbot = Chatbot(client, storage, memory, system_prompt, embedding_client, vector_store)

while True:
    question = input("\nYou: ")

    if question.lower() == "/exit":
        break

    if question.lower() == "/stats":

        stats = chatbot.get_stats()

        print(f"""
    Conversation statistics:

    Messages:          {stats["messages"]}
    Characters:        {stats["characters"]}
    Estimated tokens:  {stats["estimated_tokens"]}
    """)

        continue

    if question.lower() == "/help":
        print("""
        Available commands:

        /help     Show this help message
        /clear    Clear conversation history
        /history  Show conversation history
        /stats    Show conversation statistics
        /memory   - Show saved memories
        /forget   - Delete all saved memories
        /exit     Exit the chatbot
        """)
        continue

    if question.lower() == "/clear":
        chatbot.clear_history()
        print("\nConversation history cleared.")
        continue

    if question.lower() == "/history":
        for message in chatbot.messages:
            print(f"\n{message['role'].upper()}: {message['content']}")
        continue

    elif question == "/memory":
        print("\nAI Memory:")

        if memory.data:
            print(json.dumps(memory.data, indent=4))
            continue
        else:
            print("No saved memories.")
            continue

    elif question == "/forget":
        memory.clear()
        print("All saved memories have been cleared.")
        continue

    
    
    try:
        print("\nAI: ", end="")

        for content in chatbot.ask(question):
            print(content, end="", flush=True)

    except requests.exceptions.RequestException as e:
        print("\nAI: Could not connect to Ollama.")
        continue


    print()

    
    if chatbot.last_sources:
        print("\nSources and supporting excerpts:")

        displayed_sources = set()

        for source in chatbot.last_sources:
            filename = source["source"]

            if filename not in displayed_sources:
                displayed_sources.add(filename)

                print(f"\n- {filename}")
                print(f"  Similarity: {source['score']:.4f}")
                print(f"  Excerpt: {source['text']}")
