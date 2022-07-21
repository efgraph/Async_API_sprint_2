from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from core.error_message import PERSON_NOT_FOUND, PERSONS_NOT_FOUND, FILMS_NOT_FOUND
from services.film import FilmService, get_film_service
from models.models import Person, Film
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=list[Person], description = 'Поиск по персонам')
async def person_search(query: str = "*", page: int = Query(0, alias="page[number]", ge=0),
                        size: int = Query(50, alias="page[size]", ge=0),
                        person_service: PersonService = Depends(get_person_service)) -> list[Person]:
    persons = await person_service.search_by_query(query, page, size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSONS_NOT_FOUND)
    return persons


@router.get('/{uuid}', response_model=Person, description = 'Данные по персоне')
async def person_details(uuid: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.search(uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return person


@router.get('/{uuid}/film', response_model=list[Film], description = 'Фильмы по персоне')
async def person_film(uuid: str, page: int = Query(0, alias="page[number]", ge=0),
                      size: int = Query(50, alias="page[size]", ge=0),
                      person_service: PersonService = Depends(get_person_service),
                      film_service: FilmService = Depends(get_film_service)) -> list[Film]:
    person = await person_service.search(uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILMS_NOT_FOUND)
    ids = person.actor + person.director + person.writer
    films = await film_service.search_by_ids(person.id, ids, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILMS_NOT_FOUND)
    return films
