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
        genre = await self.redis_data_source.genre_from_cache(genre_id)
        if not genre:
            genre = await self.es_data_source.get_genre_by_id(genre_id)
            if not genre:
                return None
            await self.redis_data_source.put_genre_to_cache(genre)
        return genre

    async def search_by_query(self, query, page, size) -> list[Genre] | None:
        key = ":".join(map(str, [query, page, size]))
        genres = await self.redis_data_source.genres_from_cache(key)
        if not genres:
            genres = await self.es_data_source.get_genres_by_query(query, page, size)
            if not genres:
                return None
            await self.redis_data_source.put_genres_to_cache(key, genres)
        return genres
