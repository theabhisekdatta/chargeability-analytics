import requests
from langchain_core.embeddings import Embeddings

class JinaAPIEmbeddings(Embeddings):
    def __init__(self, api_key, model="jina-embeddings-v3"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.jina.ai/v1/embeddings"

    def embed_documents(self, texts):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "task": "retrieval.passage",
            "normalized": True,
            "input": texts
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return [
            item["embedding"]
            for item in response.json()["data"]
        ]

    def embed_query(self, text):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "task": "retrieval.query",
            "normalized": True,
            "input": [text]
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return response.json()["data"][0]["embedding"]