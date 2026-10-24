
import os
from dotenv import load_dotenv

load_dotenv()

ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
ollama_model = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")
embedding_model = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text:latest"
)
system_prompt = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful AI assistant."
)