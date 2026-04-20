import os
from typing import Literal

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    env: str = 'development'
    debug: bool = False
    LLM_PROVIDER: Literal["openai", "ollama", "anthropic"] = "ollama"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = 'llama3.2:latest' #'qwen3.5:9b'

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    #Anthropic
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-5"

    #REDIS
    REDIS_URL: str = f"{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}"


    # ======= app name ===========
    app_name: str = 'pocket_attorney_rag'

    chunker_type: str = "langchain" # simple | langchain
    chunker_size: int = 300
    chunk_overlap: int = 50

    # ===== logging ==========
    log_level: str = "INFO"
    log_to_file: bool = True
    log_file: str = "logs/app.log"
    log_max_bytes: int = 5 * 1024 * 1024
    log_backup_count: int = 5
    log_format: str = "plain"  # plain | json

settings = Settings()