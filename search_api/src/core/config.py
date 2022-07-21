import os
from logging import config as logging_config

from pydantic.env_settings import BaseSettings
from pydantic.fields import Field

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')


class Settings(BaseSettings):
    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: int = Field(6379, env='redis_port')

    elastic_host: str = Field('127.0.0.1', env='elastic_host')
    elastic_port: int = Field(9200, env='elastic_port')


settings = Settings()
