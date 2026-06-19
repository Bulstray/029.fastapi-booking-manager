from pydantic import AmqpDsn, BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = ("127.0.0.1",)
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    bookings: str = "/bookings"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn


class MessageBrokerConfig(BaseModel):
    url: AmqpDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            ".env.template",
            ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DatabaseConfig
    broker: MessageBrokerConfig

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiV1Prefix()


settings = Settings()
