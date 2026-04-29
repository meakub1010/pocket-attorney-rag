import logging

from app.core import container

logger = logging.getLogger(__name__)

class RagPipeline:
    def __init__(self, retriever, cache):
        self.retriever = retriever
        self.cache = cache

    async def query(self, question):


        results, q_embedding = await self.retriever.retrieve(question)
        logger.info("Results: ", results)
        print("Results: ", results)
        return results, q_embedding