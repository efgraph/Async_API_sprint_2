from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Query

from models.models import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/', response_model=List[Genre])
async def genres(page: int = Query(0, alias="page[number]"), size: int = Query(50, alias="page[size]"),
                 genre_service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    if size * page + size > 10000:
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail='Result window is too large')
    genres = await genre_service.search_by_query('*', page, size)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    return genres


@router.get('/{uuid}', response_model=Genre)
async def genre_details(uuid: str = '', genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre
