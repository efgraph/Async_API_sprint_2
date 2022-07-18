from pydantic import BaseSettings, Field


class PostgresConnection(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')


class ElasticConnection(BaseSettings):
    es_uri: str = Field(..., env='ELASTIC_URI')


class Etl(BaseSettings):
    state_file: str = Field(..., env="FILE_STATE_PATH")


class Settings(BaseSettings):
    postgres_conn: PostgresConnection = PostgresConnection()
    elastic_conn: ElasticConnection = ElasticConnection()
    etl_state: Etl = Etl()
