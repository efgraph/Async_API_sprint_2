import json
from functools import lru_cache
from typing import Optional, List

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.models import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def search_by_query(self, query, page, size):
        key = ":".join(map(str, ["genres", query, page, size]))
        genres = await self._genres_from_cache(key)
        if not genres:
            body = {"query": {"query_string": {"query": query}}}
            result = await self.elastic.search(index="genres", body=body, from_=page * size, size=size)
            source = [hit['_source'] for hit in result['hits']['hits']]
            genres = [Genre.to_genre(g) for g in source]
            if not genres:
                return None
            await self._put_genres_to_cache(key, genres)
        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        res = doc['_source']
        return Genre.to_genre(res)

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(genre_id)
        if not data:
            return None
        genre = Genre.parse_raw(data)
        return genre

    async def _genres_from_cache(self, key: str) -> List[Genre]:
        data = await self.redis.get(key)
        if not data:
            return None
        genres = [Genre.parse_raw(g) for g in json.loads(data)]
        return genres

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(genre.id, genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS)

    async def _put_genres_to_cache(self, key: str, genres: List[Genre]):
        await self.redis.set(key, json.dumps([g.json() for g in genres]), expire=GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(redis, elastic)
