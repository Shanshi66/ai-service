from routers import summary
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import sys
print(os.getcwd(), sys.path)


app = FastAPI()

app.include_router(summary.router)


@app.get("/")
async def hello():
    return "Hello World"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
