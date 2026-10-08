import os
from dotenv import load_dotenv

load_dotenv()

ollama_url = os.getenv("OLLAMA_URL")
ollama_model = os.getenv("OLLAMA_MODEL")
system_prompt = os.getenv("SYSTEM_PROMPT")