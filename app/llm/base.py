from abc import ABC, abstractmethod
from pydantic import BaseModel


class LLMResponse(BaseModel):
    content: str
    model: str
    usage: dict | None = None


class BaseLLMProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        pass

    @abstractmethod
    async def stream(self, prompt: str, **kwargs) -> LLMResponse:
        pass

    # @abstractmethod
    # async def embed(self, text: str) -> list[float]:
    #     pass
