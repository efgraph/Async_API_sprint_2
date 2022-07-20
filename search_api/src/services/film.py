import json
from functools import lru_cache
from typing import Optional, List

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.models import Film


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def search_by_ids(self, person_id, ids, page, size):
        key = ":".join(map(str, [person_id, page, size]))
        films = await self._films_from_cache(key)
        if not films:
            body = {"query": {"ids": {"values": ids}}}
            result = await self.elastic.search(index="movies", body=body, from_=page * size, size=size)
            source = [hit['_source'] for hit in result['hits']['hits']]
            films = [Film.to_film(f) for f in source]
            if not films:
                return None
            await self._put_films_to_cache(key, films)
        return films

    async def search_by_query(self, query, page, size):
        key = ":".join(map(str, [query, page, size]))
        films = await self._films_from_cache(key)
        if not films:
            body = {"query": {"query_string": {"query": query}}}
            result = await self.elastic.search(index="movies", body=body, from_=page * size, size=size)
            source = [hit['_source'] for hit in result['hits']['hits']]
            films = [Film.to_film(f) for f in source]
            if not films:
                return None
            await self._put_films_to_cache(key, films)
        return films

    async def get_all(self, sort, genre, page, size):
        key = ":".join(map(str, [sort, genre, page, size]))
        films = await self._films_from_cache(key)
        if not films:
            body = {"query": {"match_all": {}}}
            if sort:
                body["sort"] = [{sort: {"order": "desc"}}]
            if genre:
                body["query"] = {"bool": {"must": [{"match": {"genre": genre}}]}}
            result = await self.elastic.search(index="movies", body=body, from_=page * size, size=size)
            source = [hit['_source'] for hit in result['hits']['hits']]
            films = [Film.to_film(f) for f in source]
            if not films:
                return None
            await self._put_films_to_cache(key, films)
        return films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.hmget("movies", film_id)
        if data in [None, [None]]:
            return None
        film = Film.parse_raw(data[0])
        return film

    async def _films_from_cache(self, key: str) -> List[Film]:
        data = await self.redis.hmget("movies", key)
        if data in [None, [None]]:
            return None
        persons = [Film.parse_raw(f) for f in json.loads(data[0])]
        return persons

    async def _put_film_to_cache(self, film: Film):
        await self.redis.hmset("movies", film.id, film.json())

    async def _put_films_to_cache(self, key: str, films: List[Film]):
        await self.redis.hmset("movies", key, json.dumps([f.json() for f in films]))


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
