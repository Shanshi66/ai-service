from pydantic import BaseModel, HttpUrl
from enum import Enum


class TaskType(str, Enum):
    summary = "summary"


class ServiceRequest(BaseModel):
    doc: str
    source: HttpUrl
    task_type: TaskType
    api_token: str
    proxy_server: HttpUrl | None
