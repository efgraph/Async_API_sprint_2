import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_film(make_get_request):
    response = await make_get_request('films')
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == 50


async def test_genres(make_get_request):
    response = await make_get_request('genres')
    assert response.status == http.HTTPStatus.OK
    assert len(response.body) == 26

