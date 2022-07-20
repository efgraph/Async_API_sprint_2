import json
from functools import lru_cache
from typing import Optional, List

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.models import Person


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    async def search_by_query(self, query, page, size):
        key = ":".join(map(str, [query, page, size]))
        persons = await self._persons_from_cache(key)
        if not persons:
            body = {"query": {"query_string": {"query": query}}}
            result = await self.elastic.search(index="persons", body=body, from_=page * size, size=size)
            source = [hit['_source'] for hit in result['hits']['hits']]
            persons = [Person.to_person(p) for p in source]
            if not persons:
                return None
            await self._put_persons_to_cache(key, persons)
        return persons

    async def search(self, uuid):
        person = await self._get_person_from_elastic(uuid)
        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get('persons', person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        data = await self.redis.hmget("persons", person_id)
        if data in [None, [None]]:
            return None
        person = Person.parse_raw(data[0])
        return person

    async def _persons_from_cache(self, key: str) -> List[Person]:
        data = await self.redis.hmget("persons", key)
        if data in [None, [None]]:
            return None
        persons = [Person.parse_raw(p) for p in json.loads(data[0])]
        return persons

    async def _put_person_to_cache(self, person: Person):
        await self.redis.hmset("persons", person.id, person.json())

    async def _put_persons_to_cache(self, key: str, persons: List[Person]):
        await self.redis.hmset("persons", key, json.dumps([p.json() for p in persons]))


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(redis, elastic)
