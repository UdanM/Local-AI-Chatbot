
import chromadb

min_similarity = 0.60

class VectorStore:
    def __init__(self, path="chroma_db", collection_name="documents"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    
    def add_documents(self, documents):
        if not documents:
            return

        ids = [
            f"{document['source']}_{index}"
            for index, document in enumerate(documents)
        ]

        self.collection.upsert(
            ids=ids,
            documents=[document["text"] for document in documents],
            embeddings=[document["embedding"] for document in documents],
            metadatas=[
                {"source": document["source"]}
                for document in documents
            ]
        )

    
    def search(self, query_embedding, top_k=3, min_similarity=0.60):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count())
        )

        matches = []

        if not results["ids"] or not results["ids"][0]:
            return matches

        for index, document in enumerate(results["documents"][0]):
            score = 1 - results["distances"][0][index]

            if score < min_similarity:
                continue

            matches.append({
                "text": document,
                "source": results["metadatas"][0][index]["source"],
                "score": 1 - results["distances"][0][index]
            })

        return matches

    
    def clear(self):
        self.client.delete_collection(self.collection.name)

        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"}
        )



