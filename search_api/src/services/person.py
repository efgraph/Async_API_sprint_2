from abc import ABC, abstractmethod
from core.datasource.elastic_data_source import ESDataSource
from core.datasource.redis_data_source import RedisDataSource
from models.models import Person


class PersonService(ABC):
    @abstractmethod
    async def get_by_id(self, person_id: str) -> Person | None:
        pass

    @abstractmethod
    async def search_by_query(self, query, page, size) -> list[Person] | None:
        pass

    @abstractmethod
    async def search(self, uuid) -> Person | None:
        pass


class PersonServiceImpl(PersonService):
    def __init__(self, redis_data_source: RedisDataSource, es_data_source: ESDataSource):
        self.redis_data_source = redis_data_source
        self.es_data_source = es_data_source

    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self.redis_data_source.person_from_cache(person_id)
        if not person:
            person = await self.es_data_source.get_person_from_elastic(person_id)
            if not person:
                return None
            await self.redis_data_source.put_person_to_cache(person)
        return person

    async def search_by_query(self, query, page, size) -> list[Person] | None:
        key = ":".join(map(str, [query, page, size]))
        persons = await self.redis_data_source.persons_from_cache(key)
        if not persons:
            persons = await self.es_data_source.get_persons_by_query(query, page, size)
            if not persons:
                return None
            await self.redis_data_source.put_persons_to_cache(key, persons)
        return persons

    async def search(self, uuid) -> Person | None:
        person = await self.es_data_source.get_person_from_elastic(uuid)
        return person
