from fastapi import APIRouter
from ..models.request import ServiceRequest, TaskType
from ..models.response import ServiceResponse
from ..base.exception import CustomException
from ..ai.summary import LangChainSummaryService

router = APIRouter()


@router.post("/summary", response_model=ServiceResponse)
async def summary(request: ServiceRequest):
    if request.task_type != TaskType.summary:
        raise CustomException(
            status_code=400,
            message="Invalid task type",
        )
    summary = LangChainSummaryService.summary(
        request.doc, request.api_token, request.proxy_server)

    return ServiceResponse(
        message="Success",
        data=summary
    )
