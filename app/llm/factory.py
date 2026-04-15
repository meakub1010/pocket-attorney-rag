from functools import lru_cache

from app.core.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.providers.anthropic import AnthropicProvider
from app.llm.providers.ollama import OllamaProvider
from app.llm.providers.openai import OpenAIProvider

@lru_cache(maxsize=1)
def get_llm_provider() -> BaseLLMProvider:
    match settings.LLM_PROVIDER:
        case "openai":
            return OpenAIProvider(settings.OPENAI_API_KEY, settings.OPENAI_MODEL)
        case "ollama":
            return OllamaProvider(settings.OLLAMA_BASE_URL, settings.OLLAMA_MODEL)
        case "anthropic":
            return AnthropicProvider(settings.ANTHROPIC_BASE_URL, settings.ANTHROPIC_MODEL)
        case _:
            raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")
