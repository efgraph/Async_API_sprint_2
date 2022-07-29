import backoff
import requests
from settings.config import settings


class ESCheck:

    @backoff.on_predicate(backoff.fibo, max_value=10)
    @backoff.on_exception(backoff.expo, ConnectionError)
    def ping(self) -> bool:
        substring = "You Know, for Search".encode()
        response = requests.get(settings.elastic_host + ":" + str(settings.elastic_port))
        if substring in response.content:
            print("Elasticsearch is OK")
            return True
        else:
            print("Something went wrong, ensure the cluster is up!")
            raise ConnectionError


ESCheck().ping()
