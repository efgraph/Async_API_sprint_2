import json

from aioredis import Redis

from models.models import Genre, Person, Film


class RedisDataSource:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def genre_from_cache(self, genre_id: str) -> Genre | None:
        data = await self.redis.hmget("genres", genre_id)
        if data in [None, [None]]:
            return None
        genre = Genre.parse_raw(data[0])
        return genre

    async def genres_from_cache(self, key: str) -> list[Genre]:
        data = await self.redis.hmget("genres", key)
        if data in [None, [None]]:
            return None
        genres = [Genre.parse_raw(g) for g in json.loads(data[0])]
        return genres

    async def put_genre_to_cache(self, genre: Genre):
        await self.redis.hmset("genres", genre.id, genre.json())

    async def put_genres_to_cache(self, key: str, genres: list[Genre]):
        await self.redis.hmset("genres", key, json.dumps([g.json() for g in genres]))

    async def person_from_cache(self, person_id: str) -> Person | None:
        data = await self.redis.hmget("persons", person_id)
        if data in [None, [None]]:
            return None
        person = Person.parse_raw(data[0])
        return person

    async def persons_from_cache(self, key: str) -> list[Person]:
        data = await self.redis.hmget("persons", key)
        if data in [None, [None]]:
            return None
        persons = [Person.parse_raw(p) for p in json.loads(data[0])]
        return persons

    async def put_person_to_cache(self, person: Person):
        await self.redis.hmset("persons", person.id, person.json())

    async def put_persons_to_cache(self, key: str, persons: list[Person]):
        await self.redis.hmset("persons", key, json.dumps([p.json() for p in persons]))

    async def film_from_cache(self, film_id: str) -> Film | None:
        data = await self.redis.hmget("movies", film_id)
        if data in [None, [None]]:
            return None
        film = Film.parse_raw(data[0])
        return film

    async def films_from_cache(self, key: str) -> list[Film]:
        data = await self.redis.hmget("movies", key)
        if data in [None, [None]]:
            return None
        persons = [Film.parse_raw(f) for f in json.loads(data[0])]
        return persons

    async def put_film_to_cache(self, film: Film):
        await self.redis.hmset("movies", film.id, film.json())

    async def put_films_to_cache(self, key: str, films: list[Film]):
        await self.redis.hmset("movies", key, json.dumps([f.json() for f in films]))
