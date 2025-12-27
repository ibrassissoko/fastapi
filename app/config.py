from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_USER: str = Field(..., description="Database user name")
    DATABASE_PASSWORD: str = Field(..., description="Database user password")
    DATABASE_HOST: str = Field(..., description="Database host address")
    DATABASE_PORT: int = Field(..., description="Database port")
    DATABASE_NAME: str = Field(..., description="Database name")
    SECRET_KEY: str = Field(..., description="Secret key for JWT")
    ALGORITHM: str = Field(..., description="Algorithm for JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., description="Access token expiration time in minutes")

    class Config:
        env_file = ".env"
        extra = "forbid"


settings = Settings()
