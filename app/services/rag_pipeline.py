import json
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
        self.metadata = []
        self.index_path = index_path
        self._load_index()


    def _load_index(self):
        try:
            self.vector_store.load(self.index_path)
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
        results = self.vector_store.search(q_embedding)

        # set to cache
        # await self.cache.set(q_embedding, results)
        return results, q_embedding