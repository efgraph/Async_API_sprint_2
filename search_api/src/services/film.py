from abc import ABC, abstractmethod
from core.datasource.elastic_data_source import ESDataSource
from core.datasource.redis_data_source import RedisDataSource
from models.models import Film


class FilmService(ABC):
    @abstractmethod
    async def get_by_id(self, film_id: str) -> Film | None:
        pass

    @abstractmethod
    async def search_by_ids(self, person_id, ids, page, size) -> list[Film] | None:
        pass

    @abstractmethod
    async def search_by_query(self, query, page, size) -> list[Film] | None:
        pass


class FilmServiceImpl(FilmService):
    def __init__(self, redis_data_source: RedisDataSource, es_data_source: ESDataSource):
        self.redis_data_source = redis_data_source
        self.es_data_source = es_data_source

    async def get_by_id(self, film_id: str) -> Film | None:
        film = await self.redis_data_source.film_from_cache(film_id)
        if not film:
            film = await self.es_data_source.get_film_from_elastic(film_id)
            if not film:
                return None
            await self.redis_data_source.put_film_to_cache(film)

        return film

    async def search_by_ids(self, person_id, ids, page, size) -> list[Film] | None:
        key = ":".join(map(str, [person_id, page, size]))
        films = await self.redis_data_source.films_from_cache(key)
        if not films:
            films = await self.es_data_source.get_films_by_ids(ids, page, size)
            if not films:
                return None
            await self.redis_data_source.put_films_to_cache(key, films)
        return films

    async def search_by_query(self, query, page, size) -> list[Film] | None:
        key = ":".join(map(str, [query, page, size]))
        films = await self.redis_data_source.films_from_cache(key)
        if not films:
            films = await self.es_data_source.get_films_by_query(query, page, size)
            if not films:
                return None
            await self.redis_data_source.put_films_to_cache(key, films)
        return films

    async def get_all(self, sort, genre, page, size) -> list[Film] | None:
        key = ":".join(map(str, [sort, genre, page, size]))
        films = await self.redis_data_source.films_from_cache(key)
        if not films:
            films = await self.es_data_source.get_films_all(sort, genre, page, size)
            if not films:
                return None
            await self.redis_data_source.put_films_to_cache(key, films)
        return films
