from models.config import Config
from base import CustomException, custom_exception_handler, ErrorType, exception_to_response
from fastapi import FastAPI, Request
from routers import summary
import uvicorn
import logging

app = FastAPI()

# create v1 router
app.include_router(summary.router, prefix="/v1")
app.add_exception_handler(CustomException, custom_exception_handler)


@app.middleware("http")
async def log_header(request: Request, call_next):
    logging.debug(f"request header: {request.headers}")
    response = await call_next(request)
    return response


@app.middleware("http")
async def validate_token(request: Request, call_next):
    if Config.is_dev():
        response = await call_next(request)
        return response

    if "Authorization" not in request.headers:
        return exception_to_response(CustomException("Unauthorized", ErrorType.UNAUTHORIZED))

    token_type, _, token_info = request.headers["Authorization"].partition(" ")

    if token_type.lower() != "basic" or not Config.check_basic_token(token_info):
        return exception_to_response(CustomException("Unauthorized", ErrorType.UNAUTHORIZED))

    response = await call_next(request)
    return response


if __name__ == "__main__":
    if not Config.config_check():
        exit(1)

    logging.basicConfig(level=Config.get_log_level())

    if Config.is_dev():
        uvicorn.run(app, host="127.0.0.1", port=9000)
    elif Config.is_prod():
        uvicorn.run(app, host="0.0.0.0", port=9000)
    else:
        logging.error("please set ENV=dev or ENV=prod")
