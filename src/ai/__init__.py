from .openai import OpenAIService
from .base_llm import BaseLLM
from models import Config, LLMType
from base import AIService


class LLMFactory:
    @staticmethod
    def create(config: Config) -> AIService:
        if config.get_llm_type() == LLMType.openai:
            return OpenAIService(config)
        raise NotImplementedError
