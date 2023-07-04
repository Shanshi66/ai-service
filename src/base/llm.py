from abc import ABC, abstractmethod
from models import LLMResult, LLMConfig, LLMInput


class AIService(ABC):
    @abstractmethod
    def summary(self, llm_input: LLMInput, llm_config: LLMConfig) -> LLMResult:
        pass
