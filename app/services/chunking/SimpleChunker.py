from app.services.chunking.base import BaseChunker


class SimpleChunker(BaseChunker):
    def split(self, text: str) -> list[str]:
        print("using SimpleChunker.split")
        return [text[i : i + 100] for i in range(0, len(text), 100)]
