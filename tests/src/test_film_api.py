import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    (
            "params", "status", "body"
    ),
    (
            ("", 200, "get_all_default.json"),
            ({
                 "sort": "imdb_rating"}, 200, "get_all_sort.json"),
            ({
                 "genre": "Comedy"
             }, 200, "get_all_genre_comedy.json"),
            ({
                 "genre": "not_genre"
             }, 404, "get_all_not_found.json"),
            ({
                 "page[number]": "2"
             }, 200, "get_all_page_2.json"),
            ({
                 "page[number]": "-1"
             }, 422, "get_all_page_number_error.json"),
            ({
                 "page[size]": "-1"
             }, 422, "get_all_page_size_error.json"),
            ({
                 "genre": "Action",
                 "sort": "imdb_rating",
                 "page[number]": "5",
                 "page[size]": "10"
             }, 200, "get_all_full_parameter.json")
    )
)
async def test_film(make_get_request, read_json_data, params, status, body):
    response = await make_get_request('films', params=params)
    assert response.status == status
    if body != '':
        assert response.body == await read_json_data('film/' + body)


@pytest.mark.parametrize(
    (
            "film_id", "params", "status", "body"
    ),
    (
            ("00af52ec-9345-4d66-adbe-50eb917f463a", "", 200, "get_by_id.json"),
            ("not_found", "", 404, "get_by_id_not_found.json"),
    )
)
async def test_get_film_by_id(make_get_request, read_json_data, film_id, params, status, body):
    response = await make_get_request('films/' + film_id)
    assert response.status == status
    if body != '':
        assert response.body == await read_json_data('film/' + body)


@pytest.mark.parametrize(
    (
            "params", "status", "body"
    ),
    (
            ("", 404, "get_all_not_found.json"),
            ({
                 "query": "Star"
             }, 200, "search_star.json"),
            ({
                 "query": "Comedy",
                 "page[number]": "2",
                 "page[size]": "5"
             }, 200, "search_comedy.json")
    )
)
async def test_film_search(make_get_request, read_json_data, params, status, body):
    response = await make_get_request('films/search', params=params)
    assert response.status == status
    if body != '':
        assert response.body == await read_json_data('film/' + body)
