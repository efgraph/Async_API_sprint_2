from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.services.film import FilmService, get_film_service
from src.models.models import Person, Film
from src.services.person import PersonService, get_person_service
from fastapi_pagination import Page, paginate

router = APIRouter()


# /api/v1/films?sort=-imdb_rating
# /api/v1/films?sort=-imdb_rating&filter[genre]=<comedy-uuid> Жанр и популярные фильмы в нём. Это просто фильтрация.
# /api/v1/genres/ Список жанров.
# /api/v1/films/search/ Поиск по фильмам.
# /api/v1/persons/search/ Поиск по персонам.
# /api/v1/films/<uuid:UUID>/ Полная информация по фильму.
# /api/v1/films? Похожие фильмы.
# /api/v1/persons/<uuid:UUID>/ Данные по персоне.
# /api/v1/persons/<uuid:UUID>/film/ Фильмы по персоне.
# `/api/v1/genres/<uuid:UUID>/ Данные по конкретному жанру.
# /api/v1/films... Популярные фильмы в жанре.


@router.get('/search', response_model=Page[Person])
async def person_search(query: str = "*", person_service: PersonService = Depends(get_person_service)) -> Page[Person]:
    persons = await person_service.search_by_query(query)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')
    res = [h['_source'] for h in persons['hits']['hits']]
    return paginate(res)


@router.get('/{uuid}', response_model=Person)
async def person_details(uuid: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.search(uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/{uuid}/film', response_model=Page[Film])
async def person_film(uuid: str,
                      person_service: PersonService = Depends(get_person_service),
                      film_service: FilmService = Depends(get_film_service)) -> Page[Film]:
    person = await person_service.search(uuid)
    ids = person.actor + person.director + person.writer
    films = await film_service.search_by_ids(ids)
    res = [h['_source'] for h in films['hits']['hits']]
    result = []
    for t in res:
        f = Film(id=t['id'],
                 title=t['title'],
                 imdb_rating=t['imdb_rating'],
                 description=t['description'],
                 actors=t['actors'],
                 writers=t['writers'],
                 directors=t['director'])
        result.append(f)
    return paginate(result)



