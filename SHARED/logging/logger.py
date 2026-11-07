import logging

from SHARED.config import settings
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = settings.log_dir

FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s |"
    "%(name)s: "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logging(level: str = "INFO"):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt=FORMAT,
        datefmt=DATE_FORMAT
    )

    console =ImmediateStreamHandler()
    console.setFormatter(formatter)

    file = TimedRotatingFileHandler(
        LOG_DIR / "jarvis.log",
        when="midnight",
        backupCount=14,
        encoding="utf-8" 
    )

    file.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level.upper())

    if not getattr(root, "_jarvis_configured", False):

        root.addHandler(console)
        root.addHandler(file)

    for name in (
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi"
    ):
        external = logging.getLogger(name)
        external.handlers.clear()
        external.propagate = True
        external.setLevel(level.upper())

    logging.getLogger("jarvis").info(
        "Logging system initialized"
    )

class ImmediateStreamHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()