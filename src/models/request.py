from abc import ABC
from pydantic import BaseModel, HttpUrl
from models import ModelType, LLMType
from enum import Enum
from typing import List


class TaskType(str, Enum):
    summary = "summary"


class LLMInput(BaseModel):
    pass


class LLMConfig(BaseModel):
    model: ModelType | None
    api_token: str | None
    base_url: HttpUrl | None
    temperature: float = 0
    max_tokens: int = 300
    max_retries: int | None = 3
    llm_type: LLMType | None


class Example(BaseModel):
    human: str
    ai: str

    def count_chars(self) -> int:
        return len(self.human) + len(self.ai)


class ChatSummaryInput(LLMInput):
    system: str
    examples: List[Example] | None
    content: str

    def count_chars(self) -> int:
        result = len(self.system)
        if self.examples:
            for example in self.examples:
                result += example.count_chars()
        result += len(self.content)
        return result


class ChatSummaryRequest(BaseModel):
    llm_input: ChatSummaryInput
    llm_config: LLMConfig
