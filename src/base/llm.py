from abc import ABC, abstractmethod
from models import LLMResult, LLMInput


class AIService(ABC):
    @abstractmethod
    def summary(self, llm_input: LLMInput) -> LLMResult:
        pass
