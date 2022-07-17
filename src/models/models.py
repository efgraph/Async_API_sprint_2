from typing import List, Optional

import orjson

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Genre(BaseModel):
    id: str
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(BaseModel):
    id: str
    full_name: str
    actor: List[str] = []
    writer: List[str] = []
    director: List[str] = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[str]
    description: Optional[str]
    actors: List = []
    directors: List = []
    writers: List = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
