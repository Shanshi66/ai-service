from models.config import Config
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from routers import summary
import uvicorn
import logging

# config logger
logging.basicConfig(level=logging.DEBUG)


app = FastAPI()


# create v1 router
app.include_router(summary.router, prefix="/v1")


if __name__ == "__main__":
    if not Config.config_check():
        exit(1)
    uvicorn.run(app, host="0.0.0.0", port=8000)
