import json
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.models import Genre


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def search_by_query(self, query, page, size):
        key = ":".join(map(str, [query, page, size]))
        genres = await self._genres_from_cache(key)
        if not genres:
            body = {"query": {"query_string": {"query": query}}}
            result = await self.elastic.search(index="genres", body=body, from_=page * size, size=size)
            source = [hit['_source'] for hit in result['hits']['hits']]
            genres = [Genre(**g) for g in source]
            if not genres:
                return None
            await self._put_genres_to_cache(key, genres)
        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        res = doc['_source']
        return Genre(**res)

    async def _genre_from_cache(self, genre_id: str) -> Genre | None:
        data = await self.redis.hmget("genres", genre_id)
        if data in [None, [None]]:
            return None
        genre = Genre.parse_raw(data[0])
        return genre

    async def _genres_from_cache(self, key: str) -> list[Genre]:
        data = await self.redis.hmget("genres", key)
        if data in [None, [None]]:
            return None
        genres = [Genre.parse_raw(g) for g in json.loads(data[0])]
        return genres

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.hmset("genres", genre.id, genre.json())

    async def _put_genres_to_cache(self, key: str, genres: list[Genre]):
        await self.redis.hmset("genres", key, json.dumps([g.json() for g in genres]))


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(redis, elastic)
