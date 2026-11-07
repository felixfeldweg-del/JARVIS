from pathlib import Path, WindowsPath
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mem0_url: str = "http://192.168.178.100:8888"
    google_api_key: str = ""
    host: str = "0.0.0.0"
    port: int = 8000

    livekit_url: str = ""
    livekit_api_key: str = ""
    livekit_api_secret: str = ""

    log_dir: WindowsPath = PROJECT_ROOT / "logs"

settings = Settings()
