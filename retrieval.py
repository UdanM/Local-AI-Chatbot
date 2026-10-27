
from vector_store import VectorStore


def retrieve_chunks(question, client, vector_store, top_k=3,
                    min_similarity=0.60):
    question_vector = client.embed(question)

    return vector_store.search(
        query_embedding=question_vector,
        top_k=top_k,
        min_similarity=min_similarity
    )
