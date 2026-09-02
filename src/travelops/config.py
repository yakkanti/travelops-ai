import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class LLMConfig:
    provider: str = os.getenv("LLM_PROVIDER", "ollama")
    model: str = os.getenv("OLLAMA_MODEL", "gemma4:31b-cloud")
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    api_key: Optional[str] = os.getenv("OLLAMA_API_KEY")

settings = LLMConfig()
