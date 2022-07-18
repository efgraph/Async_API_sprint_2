from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from models.models import Film
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/search', response_model=List[Film])
async def films_search(query: str = "", page: int = Query(0, alias="page[number]"),
                       size: int = Query(50, alias="page[size]"),
                       film_service: FilmService = Depends(get_film_service)) -> List[Film]:
    if size * page + size > 10000:
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail='Result window is too large')
    films = await film_service.search_by_query(query, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films


@router.get('/', response_model=List[Film])
async def films(sort: str = "", genre: str = "", page: int = Query(0, alias="page[number]"),
                size: int = Query(50, alias="page[size]"),
                film_service: FilmService = Depends(get_film_service)) -> List[Film]:
    if size * page + size > 10000:
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail='Result window is too large')
    films = await film_service.get_all(sort, genre, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return films


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film
