from config import ollama_url, embedding_model
from vector_store import VectorStore
import json
from pathlib import Path

from chunking import chunk_text
from embeddings import EmbeddingClient


documents_path = Path("documents")
document_paths = list(documents_path.glob("*.txt"))

if not document_paths:
    raise FileNotFoundError(
        f"No .txt files found in {documents_path}"
    )

all_chunks = []

for document_path in document_paths:
    print(f"Loading {document_path}...")

    text = document_path.read_text(encoding="utf-8")
    chunks = chunk_text(text, chunk_size=300, overlap=50)

    for chunk in chunks:
        all_chunks.append({
            "text": chunk,
            "source": str(document_path)
        })

print(f"Loaded {len(document_paths)} documents.")
print(f"Created {len(all_chunks)} chunks.")


client = EmbeddingClient(
    url=ollama_url,
    model=embedding_model
)

store = VectorStore()
indexed_chunks = []

for index, chunk in enumerate(all_chunks):
    print(f"Embedding chunk {index + 1}/{len(all_chunks)}...")

    vector = client.embed(chunk["text"])

    indexed_chunks.append({
        "text": chunk["text"],
        "embedding": vector,
        "source": chunk["source"]
    })


store.clear()
store.add_documents(indexed_chunks)

print(f"\nIndexed {len(indexed_chunks)} chunks.")
print("Saved embeddings to ChromaDB.")