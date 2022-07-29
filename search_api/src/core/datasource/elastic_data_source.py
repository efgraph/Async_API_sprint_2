from typing import Callable, TypeVar

from elasticsearch import AsyncElasticsearch, NotFoundError

from models.models import Genre, Person, Film


class ESDataSource:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    T = TypeVar('T', Genre, Person, Film)

    async def get_one(self, index, id, parse: Callable[[dict], T]) -> T | None:
        try:
            doc = await self.elastic.get(index, id)
        except NotFoundError:
            return None
        res = doc['_source']
        return parse(res)

    async def get_all_by_query(self, index, query, page, size, parse: Callable[[list], list[T]]) -> list[T] | None:
        body = {"query": {"query_string": {"query": query}}}
        result = await self.elastic.search(index=index, body=body, from_=page * size, size=size)
        source = [hit['_source'] for hit in result['hits']['hits']]
        return parse(source)

    async def get_films_all(self, sort, genre, page, size) -> list[Film]:
        body = {"query": {"match_all": {}}}
        if sort:
            order = "asc" if sort[0] == '-' else "desc"
            sort = sort[1:] if sort[0] == '-' else sort
            body["sort"] = [{sort: {"order": order}}]
        if genre:
            body["query"] = {"bool": {"must": [{"match": {"genre": genre}}]}}
        result = await self.elastic.search(index="movies", body=body, from_=page * size, size=size)
        source = [hit['_source'] for hit in result['hits']['hits']]
        films = [Film(**f) for f in source]
        return films

    async def get_films_by_ids(self, ids, page, size) -> list[Film]:
        body = {"query": {"ids": {"values": ids}}}
        result = await self.elastic.search(index="movies", body=body, from_=page * size, size=size)
        source = [hit['_source'] for hit in result['hits']['hits']]
        films = [Film(**f) for f in source]
        return films
