from SHARED.logging.logger import setup_logging

setup_logging()

import uvicorn

from SHARED.config import settings
from SERVER.api.server import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "SERVER.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_config=None
    )

    