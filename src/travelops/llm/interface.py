from typing import Protocol, Any
from langchain_core.language_models import BaseChatModel

class LLMInterface(Protocol):
    def invoke(self, input: Any, config: Any = None, **kwargs) -> Any:
        ...
    
    def bind_tools(self, tools: list, **kwargs) -> Any:
        ...
    
    def with_structured_output(self, schema: Any, **kwargs) -> Any:
        ...
