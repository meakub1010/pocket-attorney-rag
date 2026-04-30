import asyncio
import json
import logging
import uuid

import faiss
import numpy as np

import redis.asyncio as redis

from app.cache.serializer import make_json_safe
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
        # self.embedder = embedder

    async def get(self, q_vec: str):
        q_vec = np.array(q_vec).astype('float32')
        faiss.normalize_L2(q_vec)
        print("index length: ", self.index.ntotal)
        if self.index.ntotal == 0:
            return None

        scores, indices = self.index.search(q_vec, 1)
        score = float(scores[0][0])
        idx = int(indices[0][0])
        if idx != -1 and score >= self.similarity_threshold:
            cache_id = self.id_map[idx]
            data = await self.redis_client.get(f"cache:{cache_id}")
            if data:
                return json.loads(data)

        return None

    async def set(self, query_vec, answer):
        cache_id = str(uuid.uuid4())[:12]
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
            safe_answer = make_json_safe(answer)
            try:
                print("set cache id: cache:", cache_id)
                await self.redis_client.set(
                    f"cache:{cache_id}",
                    json.dumps(safe_answer),
                )
            except Exception as e:
                self.logger.error(f"Redis log failed!\n{e}", exc_info=True)

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


