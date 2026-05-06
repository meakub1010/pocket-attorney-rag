class AppContainer:
    def __init__(
        self,
        llm,
        rag_pipeline,
        redis,
        semantic_cache,
        embedder,
        chunker,
        retriever,
        query_service,
        pinecone_store
    ):
        self.llm = llm
        self.rag_pipeline = rag_pipeline
        self.redis = redis
        self.semantic_cache = semantic_cache
        self.embedder = embedder
        self.chunker = chunker
        self.retriever = retriever
        self.query_service = query_service
        self.pinecone_store = pinecone_store
