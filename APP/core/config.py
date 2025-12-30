from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 1
    api_key: str = "default-static-key"
    kafka_bootstrap_servers: str = "localhost:9092"

    class Config:
        env_file = ".env"


settings = Settings()
