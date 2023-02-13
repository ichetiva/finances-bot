from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    DATABASE_URI: str | None = None
    
    @validator("DATABASE_URI", pre=True)
    def assembly_database_uri(cls, v: str, values: dict) -> str:
        if v:
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            host=values["POSTGRES_HOST"],
            path="/" + values["POSTGRES_DB"],
        )

    BOT_TOKEN: str
    
    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings


settings = get_settings()
