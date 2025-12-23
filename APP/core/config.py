from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 1
    api_key: str = "default-static-key"

    class Config:
        env_file = ".env"


settings = Settings()
