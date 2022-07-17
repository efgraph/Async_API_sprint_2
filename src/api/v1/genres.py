from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate

from src.models.models import Genre
from src.services.genre import GenreService, get_genre_service

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


@router.get('/', response_model=Page[Genre])
async def genres(genre_service: GenreService = Depends(get_genre_service)) -> Page[Genre]:
    genres = await genre_service.search_by_query('*')
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    res = [h['_source'] for h in genres['hits']['hits']]
    result = []
    for t in res:
        f = Genre(id=t['id'], name=t['genre'])
        result.append(f)

    return paginate(result)


@router.get('/{uuid}', response_model=Genre)
async def genre_details(uuid: str = '', genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre
