from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.chunking.base import BaseChunker


class LangChainChunker(BaseChunker):
    def __init__(self, chunk_size, chunk_overlap) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " "],
            keep_separator=False,
        )

    def split(self, text: str) -> list[str]:
        print("Using LangChunker.split.")
        chunks = self.splitter.split_text(text)
        print("chunks: ", chunks)
        return chunks
