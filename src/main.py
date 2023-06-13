from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .routers import summary
import uvicorn

app = FastAPI()

app.include_router(summary.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
