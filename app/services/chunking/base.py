# interface to pick chunking strategy
from abc import ABC, abstractmethod

class BaseChunker(ABC):
    @abstractmethod
    def split(self, text: str) -> list[str]:
        pass