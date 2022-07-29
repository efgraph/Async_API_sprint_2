import asyncio
import json
from multidict import CIMultiDictProxy
from dataclasses import dataclass
from pathlib import Path

import aiohttp
import pytest

from settings.urljoin import urljoin
from settings.config import settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(service: str, method: str = '', params: dict = None) -> HTTPResponse:
        params = params or {}
        url = urljoin(settings.api_url, settings.api_path, service, method)
        print(url)
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
async def read_json_data():
    async def inner(data_filename: str) -> dict:
        jsonpath = Path(Path.cwd(), 'src/assets/', data_filename)
        with jsonpath.open() as fp:
            data = json.load(fp)
        return data

    return inner
