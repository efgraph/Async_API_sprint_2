from typing import List, Optional

import orjson

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genre(BaseOrjsonModel):
    id: str
    name: str

    @staticmethod
    def to_genre(data):
        return Genre(id=data['id'], name=data['genre'])

    class Config(BaseOrjsonModel.Config):
        pass


class Person(BaseOrjsonModel):
    id: str
    full_name: str
    actor: List[str] = []
    writer: List[str] = []
    director: List[str] = []

    @staticmethod
    def to_person(data):
        return Person(
            id=data['id'],
            full_name=data['full_name'],
            actor=data['actor'],
            director=data['director'],
            writer=data['writer']
            )

    class Config(BaseOrjsonModel.Config):
        pass


class Film(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: Optional[str]
    description: Optional[str]
    genre: List = []
    actors: List = []
    directors: List = []
    writers: List = []

    @staticmethod
    def to_film(data):
        return Film(id=data['id'],
                    title=data['title'],
                    imdb_rating=data['imdb_rating'],
                    description=data['description'],
                    genre=data['genre'],
                    actors=data['actors'],
                    directors=data['director'],
                    writers=data['writers'])

    class Config(BaseOrjsonModel.Config):
        pass
