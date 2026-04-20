import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from langchain_community.cache import RedisCache

from app.api.v1.router import api_router
from app.cache.redis_client import get_redis, close_redis
from app.cache.semantic_cache import SemanticCache
from app.core.config import settings
from app.core.logger import setup_logger
from app.services.chunking.factory import get_chunker
from app.services.embedding import EmbeddingService
from app.services.rag_pipeline import RagPipeline

# ============= initialize logger ONCE when app starts
setup_logger(settings.app_name)

# ======== USE Logger ===========
logger = logging.getLogger(settings.app_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_time = time.time()
    logger.info(f"{app.title} starting")
    logger.info("Pocket Attorney RAG System API is running")
    try:
        logger.info("Initializing necessary things")
    except Exception as e:
        logger.error("Failed to initialize necessary things")
        raise e

    # REDIS
    redis_client = await get_redis()
    chunker = get_chunker()
    embedder = EmbeddingService()
    rag_pipeline = RagPipeline(embedder, chunker)
    semantic_cache = SemanticCache(redis_client, rag_pipeline.embedder)

    app.state.chunker = chunker
    app.state.embedder = embedder
    app.state.rag_pipeline = rag_pipeline
    app.state.semantic_cache = semantic_cache

    yield
    logger.info("Pocket Attorney RAG System API is shutting down")

    # close REDIS
    await close_redis()

    try:
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
