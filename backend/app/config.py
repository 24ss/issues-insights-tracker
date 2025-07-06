from pydantic_settings import BaseSettings # type: ignore
from functools import lru_cache
from pydantic import Extra

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = Extra.ignore  

@lru_cache()
def get_settings():
    return Settings()