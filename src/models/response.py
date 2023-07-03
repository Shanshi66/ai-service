from pydantic import BaseModel


class ServiceResponse(BaseModel):
    api_code: int | None = None
    message: str
    data: str | None
