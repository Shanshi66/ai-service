from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Any


class CustomException(Exception):
    def __init__(self, status_code: int, message: str, api_code: int | None = None, data: Any | None = None):
        self.status_code = status_code
        self.message = message
        self.api_code = api_code
        self.data = data


# @app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "api_code": exc.api_code,
            "data": exc.data
        }
    )
