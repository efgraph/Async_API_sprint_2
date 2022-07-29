import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    (
            "params", "status", "body"
    ),
    (
            ("", 200, "get_all_default.json"),
            ({"page[number]": "-1"}, 422, "get_all_page_number_error.json"),
            ({"page[size]": "-1"}, 422, "get_all_page_size_error.json")
    )
)
async def test_genre(make_get_request, read_json_data, params, status, body):
    response = await make_get_request('genres', params=params)
    assert response.status == status
    if body != '':
        assert response.body == await read_json_data('genre/' + body)


@pytest.mark.parametrize(
    ("genre_id", "params", "status", "body"),
    (
            ("ca124c76-9760-4406-bfa0-409b1e38d200", "", 200, "get_by_id.json"),
            ("not_found", "", 404, "get_by_id_not_found.json")
    )
)
async def test_genre_by_id(make_get_request, read_json_data, genre_id, params, status, body):
    response = await make_get_request('genres/' + genre_id)
    assert response.status == status
    if body != '':
        assert response.body == await read_json_data('genre/' + body)
