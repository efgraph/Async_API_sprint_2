import pytest


@pytest.mark.asyncio
async def test_film(make_get_request):
    response = await make_get_request('films')
    print(response)
    assert response.status == 200
    assert len(response.body) == 50


@pytest.mark.asyncio
async def test_genres(make_get_request):
    response = await make_get_request('genres')
    assert response.status == 200
    assert len(response.body) == 26

