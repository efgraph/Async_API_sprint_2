from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class Settings(BaseSettings):
    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: int = Field(6379, env='redis_port')

    elastic_host: str = Field('http://127.0.0.1', env='elastic_host')
    elastic_port: int = Field(9200, env='elastic_port')

    api_url: str = Field('http://127.0.0.1/', env='api_url')
    api_path: str = Field('api/v1/', env='api_path')


settings = Settings()
