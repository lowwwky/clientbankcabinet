from contextlib import asynccontextmanager

from fastapi import FastAPI
from api import router as api_router
import uvicorn

from core.config import settings

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:clientbank",
        host=settings.run.host,
        port=settings.run.port,
        reload=True)