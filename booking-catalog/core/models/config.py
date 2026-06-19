from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RunConfig(BaseModel):
    host: str = ("127.0.0.1",)
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    bookings: str = "/bookings"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiV1Prefix()


settings = Settings()
