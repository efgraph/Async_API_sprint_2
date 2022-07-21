from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from core.error_message import FILM_NOT_FOUND, FILMS_NOT_FOUND
from models.models import Film
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/search', response_model=list[Film], description = 'Поиск по фильмам')
async def films_search(query: str = "", page: int = Query(0, alias="page[number]", ge=0),
                       size: int = Query(50, alias="page[size]", ge=0),
                       film_service: FilmService = Depends(get_film_service)) -> list[Film]:
    films = await film_service.search_by_query(query, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILMS_NOT_FOUND)
    return films


@router.get('/', response_model=list[Film], description = 'Данные по фильмам')
async def films(sort: str = "", genre: str = "", page: int = Query(0, alias="page[number]", ge=0),
                size: int = Query(50, alias="page[size]", ge=0),
                film_service: FilmService = Depends(get_film_service)) -> list[Film]:
    films = await film_service.get_all(sort, genre, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILMS_NOT_FOUND)
    return films


@router.get('/{film_id}', response_model=Film, description = 'Полная информация по фильму')
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
    return film
