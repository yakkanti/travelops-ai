from langchain_ollama import ChatOllama
from travelops.config import settings

def create_ollama_llm():
    return ChatOllama(
        model=settings.model,
        base_url=settings.base_url,
        # ChatOllama doesn't usually take api_key in base langchain-ollama, 
        # but if using Ollama Cloud/Enterprise it might be passed via headers or environment.
        # For Phase 1 we follow standard ChatOllama.
    )
