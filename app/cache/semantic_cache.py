import asyncio
import json
import logging
import uuid

import faiss
import numpy as np

from langchain_classic.vectorstores import redis

from app.core.config import settings
from app.services.embedding import EmbeddingService


class SemanticCache:
    def __init__(
            self,
            redis_client: redis.Redis,
            embedder: EmbeddingService,
            similarity_threshold: float = 0.92,
            ttl_seconds: int = 300,
            max_cache_size: int = 10_000,

    ):
        self.redis_client = redis_client
        self.logger = logging.getLogger(settings.app_name)
        self.similarity_threshold = similarity_threshold
        self.ttl = ttl_seconds
        self.max_size = max_cache_size
        self.index = faiss.IndexFlatIP(embedder.dim)
        self.id_map = []
        self.embedder = embedder

    async def get(self, query: str):
        q_vec = self.embedder.embed([query])
        q_vec = np.array(q_vec).astype('float32')
        faiss.normalize_L2(q_vec)
        if self.index.ntotal == 0:
            return None, q_vec

        scores, indices = self.index.search(q_vec, 1)
        score = float(scores[0][0])
        idx = int(indices[0][0])

        if idx != -1 and score >= self.similarity_threshold:
            cache_id = self.id_map[idx]
            data = await self.redis_client.get_by_ids(cache_id)
            if data:
                return json.load(data), q_vec

        return None, q_vec

    async def set(self, query_vec, answer):
        print("redis cache")
        cache_id = str(uuid.uuid4())[:12]
        print(cache_id)
        query_vec = np.array(query_vec).astype("float32")
        await self.redis_client.set(
            f"cache:{cache_id}",
            json.dumps(answer),
        )
        self.index.add(query_vec)
        self.id_map.append(cache_id)

    async def set_safe(self, query_vec, answer):
        cache_id = str(uuid.uuid4())[:12]

        # REDIS Write (safe + timeout)
        async def redis_task():
            try:
                await asyncio.wait_for(
                    self.redis_client.set(
                        f"cache:{cache_id}",
                        json.dumps(answer),
                    ),
                    timeout=0.5)
            except Exception as e:
                self.logger.warning("Redis log failed!\n", e)

        # Index update
        def index_task():
            try:
                query_vec_np = np.array(query_vec).astype("float32")
                self.index.add(query_vec_np)
                self.id_map.append(cache_id)
            except Exception:
                self.logger.warning("Index update failed", exc_info=True)

        await redis_task()
        index_task()


