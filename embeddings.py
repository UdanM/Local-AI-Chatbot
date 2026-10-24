
import requests


class EmbeddingClient:
    def __init__(self, url, model):
        self.url = url.rstrip("/")
        self.model = model

    def embed(self, text):
        response = requests.post(
            f"{self.url}/api/embed",
            json={
                "model": self.model,
                "input": text
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result["embeddings"][0]