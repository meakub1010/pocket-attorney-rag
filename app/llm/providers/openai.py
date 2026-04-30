# from openai import AsyncOpenAI
from ..base import BaseLLMProvider, LLMResponse


class OpenAIProvider(BaseLLMProvider):
    pass
    # def __init__(self, api_key: str, model: str):
    #     self.client = AsyncOpenAI(api_key=api_key)
    #     self.model = model
    #
    # async def complete(self, prompt: str, **kwargs) -> LLMResponse:
    #     response = await self.client.chat.completions.create(
    #         model=self.model,
    #         messages=[{"role": "user", "content": prompt}],
    #         **kwargs
    #     )
    #     return LLMResponse(
    #         content=response.choices[0].message.content,
    #         model=self.model,
    #         usage=dict(response.usage)
    #     )
    #
    # async def stream(self, prompt: str, **kwargs):
    #     stream = await self.client.chat.completions.create(
    #         model=self.model,
    #         messages=[{"role": "user", "content": prompt}],
    #         stream=True, **kwargs
    #     )
    #     async for chunk in stream:
    #         if chunk.choices[0].delta.content:
    #             yield chunk.choices[0].delta.content
    #
    # async def embed(self, text: str) -> list[float]:
    #     response = await self.client.embeddings.create(
    #         model="text-embedding-3-small", input=text
    #     )
    #     return response.data[0].embedding
