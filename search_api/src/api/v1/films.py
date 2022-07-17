from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.models import Film
from services.film import FilmService, get_film_service
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

@router.get('/search', response_model=Page[Film])
async def films_search(query: str = "", film_service: FilmService = Depends(get_film_service)) -> Page[Film]:
    films = await film_service.search_by_query(query)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    res = [h['_source'] for h in films['hits']['hits']]
    result = []
    for t in res:
        f = Film(id=t['id'], title=t['title'],
                 imdb_rating=t['imdb_rating'],
                 description=t['description'])
        result.append(f)
    return paginate(result)


@router.get('/', response_model=Page[Film])
async def films(sort: str = "", genre: str = "",
                        film_service: FilmService = Depends(get_film_service)) -> Page[Film]:
    films = await film_service.search_by_genre(sort, genre)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
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


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film

