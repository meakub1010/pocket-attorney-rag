import logging

logger = logging.getLogger(__name__)


class RagPipeline:
    def __init__(self, retriever, embedder):
        self.retriever = retriever
        self.embedder = embedder

    async def retrieve(self, question, q_embedding):
        results = await self.retriever.retrieve(question, q_embedding)
        logger.info("Results: %s", results)
        return results

    def embed(self, question):
        return self.embedder.embed(question)
