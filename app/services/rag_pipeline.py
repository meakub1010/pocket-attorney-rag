import json

from app.services.chunking.base import BaseChunker
from app.services.chunking.factory import get_chunker
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStore


class RagPipeline:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.chunker: BaseChunker = get_chunker()

        # load data
        with open("app/data/constitution.json") as f:
            self.data = json.load(f)

        self.chunks = []
        self.metadata = []

        for item in self.data:
            text = f"""
            {item['article']}
            {item['title']}
            {item['text']}
            """
            doc_chunks = self.chunker.split(text)

            for chunk in doc_chunks:
                self.chunks.append(chunk)
                self.metadata.append({
                    "chunk": chunk,
                    "keywords": item.get("keywords", []),
                    "article": item['article'],
                    "title": item['title'],
                    "category": item['category'],
                })
        embeddings = self.embedder.embed(self.chunks)
        print("embeddings: ", embeddings[:1])
        self.vector_store = VectorStore(dim = self.embedder.dim)
        self.vector_store.add(embeddings, self.metadata)
        print("vector store: ",self.vector_store)

    def query(self, question):
        q_embedding = self.embedder.embed([question])
        results = self.vector_store.search(q_embedding)

        return results