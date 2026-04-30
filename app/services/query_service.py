import logging

from app.llm.base import LLMResponse
from app.llm.prompts.legal import build_legal_prompt
from app.utils.llm_formatter import LLMFormatter


logger = logging.getLogger(__name__)

class QueryService:
    def __init__(self, cache, rag_pipeline, llm):
        self.cache = cache
        self.rag_pipeline = rag_pipeline
        self.llm = llm

    async def ask(self, question: str):

        q_embedding = self.rag_pipeline.embed([question])

        cached_results = await self.cache.get(q_embedding)
        if cached_results:
            logger.info("cache_hit")
            return cached_results

        logger.info("cache_miss")

        results = await self.rag_pipeline.retrieve(question, q_embedding)
        if not results:
            return {
                "question": question,
                "answers": []
            }

        prompt = build_legal_prompt(question, results)
        llm_response: LLMResponse = await self.llm.complete(prompt)

        formatter_response = LLMFormatter.format_to_markdown(llm_response.content)

        results_normalized = [
            {
                "model": llm_response.model,
                "source": result["article"],
                "docs": result["answer"],
                "category": result["category"],
                "score": float(result.get("final_score") or
                               result.get("vector_score") or
                               result.get("bm25_score") or
                               0.0),
            }
            for result in results
        ]
        final_result = {
            "question": question,
            "answer": formatter_response["answer_markdown"],
            "model": llm_response.model,
            "usage": llm_response.usage,
            "sources": results_normalized,
        }
        await self.cache.set_safe(q_embedding, final_result)
        logger.info("llm_called_and_cached")
        return final_result



