from langchain_classic.vectorstores import redis


class SemanticCache:
    def __init__(
            self,
            redis_client: redis.Redis,
            similarity_threshold: float = 0.92,
            ttl_seconds: int = 300,
            max_cache_size: int = 10_000,
    ):
        self.redis_client = redis_client
        self.similarity_threshold = similarity_threshold
        self.ttl = ttl_seconds
        self.max_size = max_cache_size

