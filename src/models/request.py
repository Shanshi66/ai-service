from pydantic import BaseModel, HttpUrl
from models import ModelType
from enum import Enum
from typing import List


class TaskType(str, Enum):
    summary = "summary"


class Content(BaseModel):
    content: str
    content_key: str


class LLMInput(BaseModel):
    contents: List[Content]
    prompt_template: str | None
    output_template: str | None


class LLMConfig(BaseModel):
    model: str | None
    api_token: str | None
    base_url: HttpUrl | None
    temperature: float = 0


class ServiceRequest(BaseModel):
    llm_input: LLMInput
    llm_config: LLMConfig
    task_type: TaskType
    model: ModelType | None
