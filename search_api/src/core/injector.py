from functools import lru_cache
from elasticsearch import AsyncElasticsearch
from aioredis import Redis
import aioredis
from core.config import settings
from core.datasource.elastic_data_source import ESDataSource
from core.datasource.redis_data_source import RedisDataSource
from db import elastic, redis
from db.redis import CACHE_EXPIRE_IN_SECONDS
from fastapi import Depends

from services.film import FilmService, FilmServiceImpl
from services.genre import GenreService, GenreServiceImpl
from services.person import PersonService, PersonServiceImpl


async def get_elastic() -> AsyncElasticsearch:
    return elastic.es


async def get_redis() -> Redis:
    await redis.redis.expire("movies", CACHE_EXPIRE_IN_SECONDS)
    await redis.redis.expire("genres", CACHE_EXPIRE_IN_SECONDS)
    await redis.redis.expire("persons", CACHE_EXPIRE_IN_SECONDS)
    return redis.redis


@lru_cache()
def get_elastic_data_source(
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> ESDataSource:
    return ESDataSource(elastic)


@lru_cache()
def get_redis_data_source(
        redis: Redis = Depends(get_redis)
) -> RedisDataSource:
    return RedisDataSource(redis)


@lru_cache()
def get_person_service(
        redis_data_source: RedisDataSource = Depends(get_redis_data_source),
        es_data_source: ESDataSource = Depends(get_elastic_data_source)
) -> PersonService:
    return PersonServiceImpl(redis_data_source, es_data_source)


@lru_cache()
def get_genre_service(
        redis_data_source: RedisDataSource = Depends(get_redis_data_source),
        es_data_source: ESDataSource = Depends(get_elastic_data_source)
) -> GenreService:
    return GenreServiceImpl(redis_data_source, es_data_source)


@lru_cache()
def get_film_service(
        redis_data_source: RedisDataSource = Depends(get_redis_data_source),
        es_data_source: ESDataSource = Depends(get_elastic_data_source)
) -> FilmService:
    return FilmServiceImpl(redis_data_source, es_data_source)


async def startup():
    redis.redis = await aioredis.create_redis_pool((settings.redis_host, settings.redis_port), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.elastic_host}:{settings.elastic_port}'])


async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()
