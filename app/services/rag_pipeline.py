import json

from numpy.f2py.symbolic import normalize

from app.services.bm25_store import BM25Store
# import redis.asyncio as redis
#
# from app.cache import redis_client
# from app.cache.redis_client import get_redis
# from app.cache.semantic_cache import SemanticCache
from app.services.chunking.base import BaseChunker
from app.services.chunking.factory import get_chunker
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStore


class RagPipeline:
    def __init__(self, embedder: EmbeddingService, chunker: BaseChunker, index_path: str):
        self.embedder = embedder #EmbeddingService()
        self.chunker: BaseChunker = chunker #get_chunker()
        # self.redis: redis.Redis = get_redis()
        # self.cache = SemanticCache(self.redis, self.embedder)
        # print("Cache", self.cache)

        self.vector_store: VectorStore = VectorStore(dim=self.embedder.dim)
        self.bm25_store: BM25Store = BM25Store()

        self.metadata = []
        self.index_path = index_path
        self._load_index()


    def _load_index(self):
        try:
            self.vector_store.load(self.index_path)

            self.bm25_store.load(self.index_path)
        except Exception as e:
            raise e


        # load data
        # with open("app/data/constitution.json") as f:
        #     self.data = json.load(f)
        #
        # self.chunks = []
        # self.metadata = []
        #
        # for item in self.data:
        #     text = f"""
        #     {item['article']}
        #     {item['title']}
        #     {item['text']}
        #     """
        #     doc_chunks = self.chunker.split(text)
        #
        #     for chunk in doc_chunks:
        #         self.chunks.append(chunk)
        #         self.metadata.append({
        #             "chunk": chunk,
        #             "keywords": item.get("keywords", []),
        #             "article": item['article'],
        #             "title": item['title'],
        #             "category": item['category'],
        #         })
        # embeddings = self.embedder.embed(self.chunks)
        # print("embeddings: ", embeddings[:1])
        # self.vector_store = VectorStore(dim = self.embedder.dim)
        # self.vector_store.add(embeddings, self.metadata)
        # print("vector store: ",self.vector_store)


    async def query(self, question):
        q_embedding = self.embedder.embed([question])
        vector_results = self.vector_store.search(q_embedding, k=10)

        bm25_results = self.bm25_store.search(question, k=10)

        print("length: ", len(vector_results), len(bm25_results))

        print("BM25 results: ", bm25_results)


        # Fallback safety
        if not vector_results:
            return bm25_results
        if not bm25_results:
            return vector_results

        combined = {}
        alpha = 0.5

        # normalize scores
        v_scores = normalize(r["faiss_score"] for r in vector_results)
        b_scores = normalize(r["bm25_score"] for r in bm25_results)

        # -------------------
        # Add vector results
        # -------------------
        for r, s in zip(vector_results, v_scores):
            key = r["id"]
            combined[key] = {**r, "v_score": s, "b_score": 0}

        # -------------------
        # Add BM25 results
        # -------------------
        for r, s in zip(bm25_results, b_scores):
            key = r["id"]

            if key in combined:
                combined[key]["b_score"] = s
            else:
                combined[key] = {**r, "v_score": 0, "b_score": s}

        # -------------------
        # Final scoring
        # -------------------
        for item in combined.values():
            item["final_score"] = (
                    alpha * item["v_score"] +
                    (1 - alpha) * item["b_score"]
            )

        # sort + top k
        results = sorted(
            combined.values(),
            key=lambda x: x["final_score"],
            reverse=True
        )[:3]

        print(f"combined results: \n\n", results)


        # set to cache
        # await self.cache.set(q_embedding, results)
        return results, q_embedding