from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    backend_url: str
    api_version: str = "api/v1"
    telegram_bot_token: str
    api_key: str  # New field for API key

    model_config = ConfigDict(env_file=".env")
