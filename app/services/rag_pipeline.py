import logging

logger = logging.getLogger(__name__)

class RagPipeline:
    def __init__(self, retriever):
        self.retriever = retriever

    async def query(self, question):
        results, q_embedding = self.retriever.retrieve(question)
        logger.info("Results: ", results)
        print("Results: ", results)
        return results, q_embedding