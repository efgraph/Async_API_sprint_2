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


class PersonServiceImpl(PersonService):
    def __init__(self, redis_data_source: RedisDataSource, es_data_source: ESDataSource):
        self.redis_data_source = redis_data_source
        self.es_data_source = es_data_source

    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self.redis_data_source.get_one('persons', person_id, lambda data: Person.parse_raw(data))
        if not person:
            person = await self.es_data_source.get_one('persons', person_id, lambda data: Person(**data))
            if not person:
                return None
            await self.redis_data_source.put_one('persons', person)
        return person

    async def search_by_query(self, query, page, size) -> list[Person] | None:
        key = ":".join(map(str, [query, page, size]))
        persons = await self.redis_data_source.get_all('persons', key, lambda data: [Person.parse_raw(p) for p in data])
        if not persons:
            persons = await self.es_data_source.get_all_by_query('persons', query, page, size, lambda data: [Person(**p) for p in data])
            if not persons:
                return None
            await self.redis_data_source.put_all('persons', key, persons)
        return persons

