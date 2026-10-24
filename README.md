# Local AI Chatbot

A local AI chatbot built from scratch using Python, Ollama, and DeepSeek.

This project is part of my hands-on learning in AI engineering. I am gradually building and improving the chatbot while learning how LLM-based applications work.

## Current Features

* Local AI responses using Ollama and DeepSeek
* Streaming responses
* Persistent conversation history
* Conversation summarization
* Persistent user memory
* Automatic extraction of user information
* Intelligent memory merging
* Retrieval-Augmented Generation (RAG) for answering questions using local documents
* Document chunking and embedding generation
* Similarity-based retrieval of relevant document chunks
* Source attribution with document excerpts and similarity scores
* Terminal commands for managing conversations and memory

## Tech Stack

* Python
* Ollama
* DeepSeek R1 7B
* nomic-embed-text
* Requests
* python-dotenv
* JSON

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
├── index_documents.py
├── storage.py
├── memory.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## Running the Project

Make sure Ollama is installed and running, with the required models available:

```bash
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text
```

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
pip install -r requirements.txt
```

Create a `.env` file containing the Ollama URL, chat model, embedding model, and system prompt.

Generate the document embeddings and index:

```bash
python index_documents.py
```

Then run the chatbot:

```bash
python main.py
```

## Available Commands

```text
/help     Show available commands
/history  Show conversation history
/clear    Clear conversation history
/stats    Show conversation statistics
/memory   Show stored user memory
/forget   Clear stored user memory
/exit     Exit the chatbot
```

## Roadmap

I am continuing to develop the project and plan to explore areas such as:

* Improved memory management
* Support for multiple documents
* Tool calling
* Automated testing
* API development
* Web interface

More features will be added as the project develops.

## Why I Built This

The goal of this project is to gain practical experience building LLM applications rather than simply using an existing chatbot framework.

I am using Ollama and DeepSeek so that the core application can run locally while I experiment with different AI engineering concepts.