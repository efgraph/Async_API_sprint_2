import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ("person_id", "params", "status", "body"),
    (
            ("9ea3f318-841d-44fc-afba-21d154eb99be", "", 200, "get_by_id.json"),
            ("not_found", "", 404, "get_by_id_not_found.json")
    )
)
async def test_person_by_id(make_get_request, read_json_data, person_id, params, status, body):
    response = await make_get_request('persons/' + person_id)
    assert response.status == status
    if body != '':
        assert response.body == await read_json_data('person/' + body)


@pytest.mark.parametrize(
    ("params", "status", "body"),
    (
            ("", 200, "get_arbitrary.json"),
            ({
                 "query": "Jennifer"
             }, 200, "search_jennifer.json"),
            ({
                 "query": "Tom",
                 "page[number]": "2",
                 "page[size]": "5"
             }, 200, "search_tom.json")
    )
)
async def test_person_search(make_get_request, read_json_data, params, status, body):
    response = await make_get_request('persons/search', params=params)
    assert response.status == status
    if body != '':
        assert response.body == await read_json_data('person/' + body)


@pytest.mark.parametrize(
    ("person_id", "params", "status", "body"),
    (
            ("9ea3f318-841d-44fc-afba-21d154eb99be", "", 200, "get_person_film_by_id.json"),
            ("not_found", "", 404, "get_person_film_not_found.json")
    )
)
async def test_person_film(make_get_request, read_json_data, person_id, params, status, body):
    response = await make_get_request('persons/' + person_id + '/film')
    assert response.status == status
    if body != '':
        assert response.body == await read_json_data('person/' + body)
