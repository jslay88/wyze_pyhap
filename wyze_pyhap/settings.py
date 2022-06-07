from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    LOG_LEVEL: Optional[str] = Field(default="INFO", env="LOG_LEVEL")

    WYZE_USERNAME: Optional[str] = Field(default=None, env="WYZE_USERNAME")
    WYZE_PASSWORD: Optional[str] = Field(default=None, env="WYZE_PASSWORD")
    WYZE_TOTP: Optional[str] = Field(default=None, env="WYZE_TOTP")
    BIND_ADDRESS: Optional[str] = Field(default=None, env="BIND_ADDRESS")
    BIND_INTERFACE_NAME: Optional[str] = Field(default=None, env="BIND_INTERFACE_NAME")
    ACCESSORY_STATE_PATH: str = Field(
        default="accessory.state", env="ACCESSORY_STATE_PATH"
    )


settings = Settings()
