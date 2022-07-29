from aioredis import Redis

redis: Redis | None = None

CACHE_EXPIRE_IN_SECONDS = 60 * 5
