from app.llm.base import BaseLLMProvider


# llm/providers/anthropic.py
#import anthropic
from ..base import BaseLLMProvider, LLMResponse

class AnthropicProvider(BaseLLMProvider):
    pass
    # def __init__(self, api_key: str, model: str):
    #     self.client = anthropic.AsyncAnthropic(api_key=api_key)
    #     self.model = model
    #
    # async def complete(self, prompt: str, **kwargs) -> LLMResponse:
    #     response = await self.client.messages.create(
    #         model=self.model,
    #         max_tokens=kwargs.get("max_tokens", 1024),
    #         messages=[{"role": "user", "content": prompt}]
    #     )
    #     return LLMResponse(
    #         content=response.content[0].text,
    #         model=self.model,
    #         usage={
    #             "input_tokens":  response.usage.input_tokens,
    #             "output_tokens": response.usage.output_tokens,
    #         }
    #     )
    #
    # async def stream(self, prompt: str, **kwargs):
    #     async with self.client.messages.stream(
    #         model=self.model,
    #         max_tokens=kwargs.get("max_tokens", 1024),
    #         messages=[{"role": "user", "content": prompt}]
    #     ) as stream:
    #         async for text in stream.text_stream:
    #             yield text
    #
    # async def embed(self, text: str) -> list[float]:
    #     # Anthropic doesn't have an embeddings API
    #     # raise to force caller to use a different provider for embeddings
    #     raise NotImplementedError(
    #         "Anthropic does not provide an embeddings API. "
    #         "Use SentenceTransformer or OpenAI for embeddings."
    #     )