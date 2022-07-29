from abc import ABC, abstractmethod
from core.datasource.elastic_data_source import ESDataSource
from core.datasource.redis_data_source import RedisDataSource
from models.models import Genre


class GenreService(ABC):
    @abstractmethod
    async def get_by_id(self, genre_id: str) -> Genre | None:
        pass

    @abstractmethod
    async def search_by_query(self, query, page, size) -> list[Genre] | None:
        pass


class GenreServiceImpl(GenreService):
    def __init__(self, redis_data_source: RedisDataSource, es_data_source: ESDataSource):
        self.redis_data_source = redis_data_source
        self.es_data_source = es_data_source

    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre = await self.redis_data_source.get_one('genres', genre_id, lambda data: Genre.parse_raw(data))
        if not genre:
            genre = await self.es_data_source.get_one('genres', genre_id, lambda data: Genre(**data))
            if not genre:
                return None
            await self.redis_data_source.put_one('genres', genre)
        return genre

    async def search_by_query(self, query, page, size) -> list[Genre] | None:
        key = ":".join(map(str, [query, page, size]))
        genres = await self.redis_data_source.get_all('genres', key, lambda data : [Genre.parse_raw(g) for g in data])
        if not genres:
            genres = await self.es_data_source.get_all_by_query('genres', query, page, size, lambda data: [Genre(**g) for g in data])
            if not genres:
                return None
            await self.redis_data_source.put_all('genres', key, genres)
        return genres
