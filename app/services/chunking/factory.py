from app.core.config import settings
from app.services.chunking.LangChainChunker import LangChainChunker
from app.services.chunking.SimpleChunker import SimpleChunker


def get_chunker():
    if settings.chunker_type == "langchain":
        return LangChainChunker(settings.chunker_size, settings.chunk_overlap)
    return SimpleChunker()
