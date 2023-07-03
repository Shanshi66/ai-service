from fastapi import APIRouter, Depends
from models import ServiceResponse, ServiceRequest, LLMResponse, TaskType
from base import CustomException, ErrorType
from models import Config
from ai import LLMFactory

router = APIRouter()


@router.post("/summary", response_model=ServiceResponse)
async def summary(request: ServiceRequest, config: Config = Depends()):
    if request.task_type != TaskType.summary:
        raise CustomException(
            message=f"task type shoud be {TaskType.summary}",
            error_type=ErrorType.WRONG_TASK_TYPE
        )

    llm_result = LLMFactory.create(config, request.llm_config).summary(
        request.llm_input
    )

    return ServiceResponse(
        message="Success",
        data=LLMResponse(
            llm_type=config.get_llm_type(),
            result=[llm_result]
        )
    )
