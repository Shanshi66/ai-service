from fastapi import APIRouter, Depends
from models.request import ServiceRequest, TaskType
from models.response import ServiceResponse
from base import CustomException
from models import Config
from ai import LLMFactory

router = APIRouter()


@router.post("/summary", response_model=ServiceResponse)
async def summary(request: ServiceRequest, config: Config = Depends()):
    if request.task_type != TaskType.summary:
        raise CustomException(
            status_code=400,
            message="Invalid task type",
        )

    summary = LLMFactory.create(config).summary(
        request.content,
    )

    return ServiceResponse(
        message="Success",
        data=summary
    )
