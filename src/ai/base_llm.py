from enum import Enum
from models import Config, LLMType
from base import AIService


class BaseLLM:
    def __init__(self, config: Config):
        self.api_token = config.get_token()
        self.base_url = config.get_base_url()
