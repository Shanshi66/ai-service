from pydantic import BaseModel, HttpUrl
from enum import Enum


class TaskType(str, Enum):
    summary = "summary"


class ServiceRequest(BaseModel):
    content: str
    content_key: str | None  # content_key is used to identify the content, and use for cache
    task_type: TaskType
    api_token: str | None
    base_url: HttpUrl | None
    prompt_template: str | None
    output_template: str | None
