from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from services.film import FilmService, get_film_service
from models.models import Person, Film
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=List[Person])
async def person_search(query: str = "*", page: int = Query(0, alias="page[number]"),
                        size: int = Query(50, alias="page[size]"),
                        person_service: PersonService = Depends(get_person_service)) -> List[Person]:
    if size * page + size > 10000:
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail='Result window is too large')
    persons = await person_service.search_by_query(query, page, size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')
    return persons


@router.get('/{uuid}', response_model=Person)
async def person_details(uuid: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.search(uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/{uuid}/film', response_model=List[Film])
async def person_film(uuid: str, page: int = Query(0, alias="page[number]"),
                      size: int = Query(50, alias="page[size]"),
                      person_service: PersonService = Depends(get_person_service),
                      film_service: FilmService = Depends(get_film_service)) -> List[Film]:
    if size * page + size > 10000:
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail='Result window is too large')
    person = await person_service.search(uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    ids = person.actor + person.director + person.writer
    films = await film_service.search_by_ids(ids, page, size)
    return films
