from contextlib import asynccontextmanager

from fastapi import FastAPI

from SHARED.config import settings
from SERVER.memory.mem0 import Mem0Client


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.mem0 = Mem0Client(settings.mem0_url)

    yield 

    await app.state.mem0.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="JARVIS API",
        version="1.0.0",
    )

    @app.get("/")
    async def root():
        return{
            "name": "JARVIS",
            "status":"online"
        }
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy"
        }

    return app