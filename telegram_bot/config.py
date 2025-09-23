from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    app_name: str
    debug: bool = False
    api_base: str
    api_version: str = "api/v1"
    telegram_bot_token: str

    model_config = ConfigDict(env_file=".env")
