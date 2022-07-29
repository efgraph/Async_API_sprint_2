import pytest


@pytest.mark.asyncio
async def test_person_by_id(make_get_request, read_json_data):
    config = await read_json_data('person/config_get_by_id.json')
    for test in config:
        response = await make_get_request('persons/' + test['person_id'])
        assert response.status == test['status']
        if test['body'] != '':
            assert response.body == await read_json_data('person/' + test['body'])


@pytest.mark.asyncio
async def test_person_search(make_get_request, read_json_data):
    config = await read_json_data('person/config_search.json')
    for test in config:
        response = await make_get_request('persons/search', params=test['parameter'])
        assert response.status == test['status']
        if test['body'] != '':
            assert response.body == await read_json_data('person/' + test['body'])


@pytest.mark.asyncio
async def test_person_film(make_get_request, read_json_data):
    config = await read_json_data('person/config_person_film.json')
    for test in config:
        response = await make_get_request('persons/' + test['person_id'] + '/film')
        assert response.status == test['status']
        if test['body'] != '':
            assert response.body == await read_json_data('person/' + test['body'])
