from .openai import OpenAIService
from .base_llm import BaseLLM
from models import Config, LLMType, LLMConfig
from base import AIService


class LLMFactory:
    @staticmethod
    def create(config: Config, llm_config: LLMConfig) -> AIService:
        if config.get_llm_type() == LLMType.openai:
            return OpenAIService(config, llm_config)
        raise NotImplementedError
