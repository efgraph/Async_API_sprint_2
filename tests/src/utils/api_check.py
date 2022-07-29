import backoff

import requests
from requests.exceptions import ConnectionError

from settings.config import settings


class ApiCheck:

    @backoff.on_predicate(backoff.fibo, max_value=10)
    @backoff.on_exception(backoff.expo, ConnectionError)
    def ping(self) -> bool:
        response = requests.get(settings.api_url + 'api/v1/films')
        if response.status_code == 200:
            return True
        return False


ApiCheck().ping()
