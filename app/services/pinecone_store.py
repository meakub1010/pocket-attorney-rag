import logging

from langchain_community.vectorstores import Pinecone

from app.services.embedding import EmbeddingService

logger = logging.getLogger(__name__)

class PineconeStore:
    def __init__(self, pc: Pinecone, index_name: str, embedder: EmbeddingService):
        self.pc = pc
        self.index = pc.Index(index_name)
        self.embedder = embedder

    def search(self, query, k=5, threshold=0.45):
        query_embedding = self.embedder.embed(query)

        results = self.index.query(vector=query_embedding, top_k=k, include_metadata=True)

        output = []

        for match in results.matches:
            if match.score < threshold:
                continue

            output.append({
                "id": match.id,
                "answer": match.metadata.get("chunk", ""),
                "article": match.metadata.get("article", ""),
                "title": match.metadata.get("title", ""),
                "category": match.metadata.get("category", ""),
                "faiss_score": match.score
            })
        logger.info("pinecone_results_count=%d", len(output))

        return output