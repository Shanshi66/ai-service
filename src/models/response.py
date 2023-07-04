from pydantic import BaseModel
from typing import List
from models import LLMType


class Usage(BaseModel):
    total_tokens: int
    total_cost: float
    prompt_tokens: int
    completion_tokens: int


class LLMResult(BaseModel):
    content_key: str
    result: str
    usage: Usage
    model: str


class LLMResponse(BaseModel):
    llm_type: LLMType
    result: List[LLMResult]


class ServiceResponse(BaseModel):
    api_code: int | None = None
    message: str
    data: LLMResponse | None
