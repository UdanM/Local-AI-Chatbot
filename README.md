# Local AI Chatbot

A local AI chatbot built from scratch using Python, Ollama, and DeepSeek. The project combines conversational memory with Retrieval-Augmented Generation (RAG) to answer questions using local documents.

## Features

- Local AI responses using Ollama and DeepSeek R1 7B
- Streaming responses
- Persistent conversation history
- Conversation summarization
- Persistent user memory with automatic information extraction and merging
- Retrieval-Augmented Generation (RAG) for answering questions using local documents
- Document chunking and embedding generation
- Vector storage and similarity-based retrieval using ChromaDB
- Source attribution with document excerpts and similarity scores
- Terminal commands for managing conversations and memory

## Tech Stack

- Python
- Ollama
- DeepSeek R1 7B
- nomic-embed-text
- ChromaDB
- Requests
- python-dotenv
- JSON

## Project Structure

```text
local-ai-chatbot/
│
├── documents/
│   └── university_rules.txt
├── chatbot.py
├── ollama_client.py
├── embeddings.py
├── chunking.py
├── retrieval.py
├── vector_store.py
├── index_documents.py
├── storage.py
├── memory.py
├── config.py
├── main.py
├── test_vector_store.py
├── requirements.txt
└── README.md
```

## Requirements

- Python
- [Ollama](https://ollama.com/)
- The DeepSeek R1 7B and nomic-embed-text models

Download the required models:

```bash
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text
```

## Setup

Clone the repository and navigate to the project directory.

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with the Ollama URL, chat model, embedding model, and system prompt.

## Index Documents

Place your text documents in the `documents/` directory. Generate their embeddings and store them in ChromaDB:

```bash
python index_documents.py
```

This creates or rebuilds the local `chroma_db/` database. The database is generated locally and does not need to be downloaded or committed to Git.

Run this command again whenever you want to rebuild the index after changing the source documents.

## Run the Chatbot

Make sure Ollama is running, then execute:

```bash
python main.py
```

Ask questions about the indexed documents. When relevant information is retrieved, the chatbot displays the source document and supporting excerpts.

## Available Commands

| Command | Description |
|---|---|
| `/help` | Show available commands |
| `/history` | Show conversation history |
| `/clear` | Clear conversation history |
| `/stats` | Show conversation statistics |
| `/memory` | Show stored user memory |
| `/forget` | Clear stored user memory |
| `/exit` | Exit the chatbot |

## Contributors

Udan Marapperuma - udanmarapperuma@gmail.com