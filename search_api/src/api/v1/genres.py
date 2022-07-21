from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request, Query

from core.error_message import GENRE_NOT_FOUND, GENRES_NOT_FOUND
from models.models import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/', response_model=list[Genre], description = 'Список жанров')
async def genres(page: int = Query(0, alias="page[number]", ge=0), size: int = Query(50, alias="page[size]", ge=0),
                 genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    genres = await genre_service.search_by_query('*', page, size)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRES_NOT_FOUND)
    return genres


@router.get('/{uuid}', response_model=Genre, description = 'Данные по конкретному жанру')
async def genre_details(uuid: str = '', genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)
    return genre
