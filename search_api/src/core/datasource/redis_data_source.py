import json
from typing import TypeVar, Callable

from aioredis import Redis

from models.models import Genre, Person, Film


class RedisDataSource:
    def __init__(self, redis: Redis):
        self.redis = redis

    T = TypeVar('T', Genre, Person, Film)

    async def get_one(self, index, key, parse: Callable[[str], T]) -> T | None:
        data = await self.redis.hmget(index, key)
        if data in [None, [None]]:
            return None
        return parse(data[0])

    async def get_all(self, index: str, key: str, parse: Callable[[str], list[T]]) -> list[T] | None:
        data = await self.redis.hmget(index, key)
        if data in [None, [None]]:
            return None
        return parse(json.loads(data[0]))

    async def put_one(self, index: str, obj: T):
        await self.redis.hmset(index, obj.id, obj.json())

    async def put_all(self, index, key, obj_list: list[T]):
        await self.redis.hmset(index, key, json.dumps([o.json() for o in obj_list]))
