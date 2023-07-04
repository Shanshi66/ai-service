from abc import ABC
from pydantic import BaseModel, HttpUrl
from models import ModelType
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
    max_tokens: int = 100
    max_retries: int = 3


class ExampleMessage(BaseModel):
    human_message: str
    ai_message: str


class ChatSummaryInput(LLMInput):
    system_message: str
    example_messages: List[ExampleMessage] | None
    content: str


class ChatSummaryRequest(BaseModel):
    llm_input: ChatSummaryInput
    llm_config: LLMConfig
