from pydantic import BaseModel
from typing import List
from models import LLMType


class Usage(BaseModel):
    total_tokens: int
    total_cost: float
    prompt_tokens: int
    completion_tokens: int


class LLMResult(BaseModel):
    result: str
    usage: Usage
    model: str
    llm_type: LLMType


class ServiceResponse(BaseModel):
    api_code: int | None = None
    message: str
    data: LLMResult | None = None
