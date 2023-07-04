from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Any
from enum import Enum
from models import ServiceResponse


# error type include status code and api code
class ErrorType(tuple[int, int], Enum):
    # client error
    WRONG_TASK_TYPE = (status.HTTP_400_BAD_REQUEST, 1001)

    # server error
    NOT_SUPPORT = (status.HTTP_500_INTERNAL_SERVER_ERROR, 2001)
    LLM_NETWORK_ERROR = (status.HTTP_500_INTERNAL_SERVER_ERROR, 2002)


class CustomException(Exception):
    def __init__(self, message: str, error_type: ErrorType):
        self.message = message
        self.error_type = error_type


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.error_type[0],
        content={
            "message": exc.message,
            "api_code": exc.error_type[1],
        }
    )
