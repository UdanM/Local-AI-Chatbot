
import math


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)



def retrieve_chunks(
    question,
    indexed_chunks,
    client,
    top_k=3,
    min_similarity=0.50
):
    question_vector = client.embed(question)

    scored_chunks = []

    for item in indexed_chunks:
        score = cosine_similarity(
            question_vector,
            item["embedding"]
        )

        scored_chunks.append({
            "text": item["text"],
            "source": item["source"],
            "score": score
        })

    scored_chunks = [
        item for item in scored_chunks
        if item["score"] >= min_similarity
    ]

    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return scored_chunks[:top_k]

