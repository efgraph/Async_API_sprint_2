import backoff
from settings.config import settings
from redis import Redis


class CacheCheck:
    def __init__(self):
        self.redis = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True
        )

    @backoff.on_predicate(backoff.fibo, max_value=10)
    @backoff.on_exception(backoff.expo, ConnectionError)
    def ping(self) -> bool:
        if self.redis.ping():
            print("Redis is OK")
            return True
        return False


CacheCheck().ping()
