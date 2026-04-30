import httpx
import json

from app.llm.base import BaseLLMProvider, LLMResponse


class OllamaProvider(BaseLLMProvider):
    def __init__(self, base_url: str, aimodel: str):
        self.base_url = base_url
        self.model = aimodel
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(connect=5, read=180.0, write=15.0, pool=5.0)
        )

    async def _post(self, endpoint: str, payload: dict):
        url = f"{self.base_url}{endpoint}"
        print("calling: ", url)
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         f"{self.base_url}/api/generate",
        #         json={"model": self.model, "prompt": prompt, "stream": False},
        #         timeout=180.0,
        #     )
        #     data = response.json()
        #     return LLMResponse(content=data["response"], model= self.model)
        endpoint = "/api/generate"
        data = await self._post(
            endpoint, {"model": self.model, "prompt": prompt, "stream": False}
        )
        return LLMResponse(
            content=data.get("response", ""),
            model=self.model,
            usage=data.get("usage", None),
        )

    async def stream(self, prompt: str, **kwargs):
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": True},
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        if not data.get("done"):
                            yield data.get("response", "")

    # async def embed(self, text: str) -> list[float]:
    #     async with httpx.AsyncClient() as client:
    #         response = await client.post(
    #             f"{self.base_url}/api/embeddings",
    #             json={"model": self.model, "prompt": text},
    #         )
    #         return response.json()["embedding"]
