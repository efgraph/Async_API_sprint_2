import orjson

from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True


class Genre(BaseOrjsonModel):
    id: str
    name: str = Field(alias='genre')


class Person(BaseOrjsonModel):
    id: str
    full_name: str
    actor: list[str] = Field(default=[])
    writer: list[str] = []
    director: list[str] = []


class Film(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: str | None
    description: str | None
    genre: list = []
    actors: list = []
    directors: list = Field(default=[], alias='director')
    writers: list = []
