from fastapi import FastAPI

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