from elasticsearch import AsyncElasticsearch, NotFoundError

from models.models import Genre, Person, Film


class ESDataSource:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_genre_by_id(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        res = doc['_source']
        return Genre(**res)

    async def get_genres_by_query(self, query, page, size) -> list[Genre]:
        body = {"query": {"query_string": {"query": query}}}
        result = await self.elastic.search(index="genres", body=body, from_=page * size, size=size)
        source = [hit['_source'] for hit in result['hits']['hits']]
        genres = [Genre(**g) for g in source]
        return genres

    async def get_person_from_elastic(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get('persons', person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def get_persons_by_query(self, query, page, size) -> list[Person]:
        body = {"query": {"query_string": {"query": query}}}
        result = await self.elastic.search(index="persons", body=body, from_=page * size, size=size)
        source = [hit['_source'] for hit in result['hits']['hits']]
        persons = [Person(**p) for p in source]
        return persons

    async def get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def get_films_all(self, sort, genre, page, size) -> list[Film]:
        body = {"query": {"match_all": {}}}
        if sort:
            body["sort"] = [{sort: {"order": "desc"}}]
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

    async def get_films_by_query(self, query, page, size) -> list[Film]:
        body = {"query": {"query_string": {"query": query}}}
        result = await self.elastic.search(index="movies", body=body, from_=page * size, size=size)
        source = [hit['_source'] for hit in result['hits']['hits']]
        films = [Film(**f) for f in source]
        return films
