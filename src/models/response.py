from pydantic import BaseModel
from typing import List
from models import LLMType


class LLMResult(BaseModel):
    content_key: str
    result: str
    token_usage: int
    model: str


class LLMResponse(BaseModel):
    llm_type: LLMType
    result: List[LLMResult]


class ServiceResponse(BaseModel):
    api_code: int | None = None
    message: str
    data: LLMResponse | None
