import pytest


@pytest.mark.asyncio
async def test_film(make_get_request, read_json_data):
    config = await read_json_data('film/config_get_all.json')
    for test in config:
        response = await make_get_request('films', params=test['parameter'])
        assert response.status == test['status']
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body'])


@pytest.mark.asyncio
async def test_get_film_by_id(make_get_request, read_json_data):
    config = await read_json_data('film/config_get_by_id.json')
    for test in config:
        response = await make_get_request('films/' + test['film_id'])
        assert response.status == test['status']
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body'])


@pytest.mark.asyncio
async def test_film_search(make_get_request, read_json_data):
    config = await read_json_data('film/config_search.json')
    for test in config:
        response = await make_get_request('films/search', params=test['parameter'])
        assert response.status == test['status']
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body'])
