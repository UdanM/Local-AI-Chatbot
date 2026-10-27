
from config import ollama_url, embedding_model
from embeddings import EmbeddingClient
from vector_store import VectorStore

embedding_client = EmbeddingClient(
    url=ollama_url,
    model=embedding_model
)

store = VectorStore()

question = "How many times can I retake a failed exam?"
question_embedding = embedding_client.embed(question)

results = store.search(
    query_embedding=question_embedding,
    top_k=3
)

for result in results:
    print(f"\nSource: {result['source']}")
    print(f"Similarity: {result['score']:.4f}")
    print(f"Text: {result['text']}")
