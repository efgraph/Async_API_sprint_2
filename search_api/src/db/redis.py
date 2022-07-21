from aioredis import Redis

redis: Redis | None = None

CACHE_EXPIRE_IN_SECONDS = 60 * 5


async def get_redis() -> Redis:
    await redis.expire("movies", CACHE_EXPIRE_IN_SECONDS)
    await redis.expire("genres", CACHE_EXPIRE_IN_SECONDS)
    await redis.expire("persons", CACHE_EXPIRE_IN_SECONDS)
    return redis