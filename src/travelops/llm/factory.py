from typing import Any
from travelops.config import settings
from travelops.llm.ollama import create_ollama_llm

class MockLLM:
    """
    A deterministic Mock LLM that mimics LangChain's ChatModel interface.
    """
    def __init__(self, model_name: str):
        self.model_name = model_name

    def invoke(self, input: Any, config: Any = None, **kwargs):
        # Mock response based on input content
        # In a real implementation, this would look at the prompt and return specific mock data
        return "Mock response from Gemma 4"

    def bind_tools(self, tools: list, **kwargs):
        return self

    def with_structured_output(self, schema: Any, **kwargs):
        # Return a mock object that mimics the schema
        return self

class LLMFactory:
    @staticmethod
    def get_llm():
        provider = settings.provider
        
        if provider == "ollama":
            return create_ollama_llm()
        elif provider == "mock":
            return MockLLM(settings.model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
