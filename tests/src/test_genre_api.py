import pytest


@pytest.mark.asyncio
async def test_genre(make_get_request, read_json_data):
    config = await read_json_data('genre/config_get_all.json')
    for test in config:
        response = await make_get_request('genres', params=test['parameter'])
        assert response.status == test['status']
        if test['body'] != '':
            assert response.body == await read_json_data('genre/' + test['body'])


@pytest.mark.asyncio
async def test_genre_by_id(make_get_request, read_json_data):
    config = await read_json_data('genre/config_get_by_id.json')
    for test in config:
        response = await make_get_request('genres/' + test['genre_id'])
        assert response.status == test['status']
        if test['body'] != '':
            assert response.body == await read_json_data('genre/' + test['body'])
