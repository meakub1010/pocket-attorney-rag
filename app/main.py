import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.cache.redis_client import get_redis, close_redis
from app.cache.semantic_cache import SemanticCache
from app.core.config import settings
from app.core.container import AppContainer
from app.core.logger import setup_logger
from app.llm.factory import get_llm_provider
from app.services.bm25_store import BM25Store
from app.services.chunking.factory import get_chunker
from app.services.embedding import EmbeddingService
from app.services.rag_pipeline import RagPipeline
from app.services.retrievers.hybrid_retriever import HybridRetriever
from app.services.vector_store import VectorStore

# ============= initialize logger ONCE when app starts
setup_logger(settings.app_name)

# ======== USE Logger ===========
logger = logging.getLogger(settings.app_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_time = time.time()
    logger.info(f"{app.title} starting")
    try:
        logger.info("Initializing necessary things")
        # REDIS
        redis_client = await get_redis()
        chunker = get_chunker()
        embedder = EmbeddingService()

        vector_store = VectorStore(dim=embedder.dim)
        vector_store.load(settings.index_path)

        bm25_store = BM25Store()
        bm25_store.load(settings.index_path)

        retriever = HybridRetriever(vector_store, bm25_store, embedder)

        rag_pipeline = RagPipeline(retriever)

        semantic_cache = SemanticCache(redis_client, embedder)
        llm_client = get_llm_provider()

        container = AppContainer(
            llm = llm_client,
            rag_pipeline=rag_pipeline,
            redis=redis_client,
            semantic_cache=semantic_cache,
            embedder=embedder,
            chunker=chunker,
            retriever = retriever
        )

        app.state.container = container
        logger.info(f"All services has been initialized")
    except Exception as e:
        logger.error("Failed to initialize necessary services")
        raise e
    yield
    try:
        logger.info("Pocket Attorney RAG System API is shutting down")

        # close REDIS
        await close_redis()

        # llm close
        if hasattr(llm_client, "close"):
            await llm_client.close()
        elapsed_time = time.time() - start_time
        logger.info(f"Clean up complete. Uptime: {elapsed_time:.2f}s")
    except Exception as e:
        logger.error("Error during shutdown")

app = FastAPI(
    title="Pocket Attorney System API",
    description="Pocket Attorney RAG System API",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(api_router, prefix="/api/v1")

# quick health check

@app.get("/")
async def root():
    return {"status": "ok", "message": "Pocket Attorney RAG System API is running"}


# # ========= APP EVENTS ================
# @app.on_event("startup")
# async def startup():
#     logger.info("Pocket Attorney RAG System API is running")
#
# @app.on_event("shutdown")
# async def shutdown():
#     logger.info("Pocket Attorney RAG System API is shutting down")


#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
