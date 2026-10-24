
import json
from pathlib import Path

from chunking import chunk_text
from embeddings import EmbeddingClient


document_path = Path("documents/university_rules.txt")
text = document_path.read_text(encoding="utf-8")

chunks = chunk_text(text, chunk_size=300, overlap=50)

client = EmbeddingClient(
    url="http://localhost:11434",
    model="nomic-embed-text"
)

indexed_chunks = []

for index, chunk in enumerate(chunks):
    print(f"Embedding chunk {index + 1}/{len(chunks)}...")

    vector = client.embed(chunk)

    indexed_chunks.append({
        "text": chunk,
        "embedding": vector,
        "source": str(document_path)
    })

store_path = Path("vector_store.json")
store_path.write_text(
    json.dumps(indexed_chunks, indent=2),
    encoding="utf-8"
)

print(f"\nIndexed {len(indexed_chunks)} chunks.")
print(f"Saved embeddings to {store_path}.")
