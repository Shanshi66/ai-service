from pydantic import BaseModel
from typing import Optional


class ServiceResponse(BaseModel):
    api_code: int | None = None
    message: str
    data: str | None
