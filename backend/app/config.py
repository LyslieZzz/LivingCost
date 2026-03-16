from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://root:password@localhost:3306/livingcost"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    cors_origins: str = "http://localhost:3000,http://localhost:8080"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
