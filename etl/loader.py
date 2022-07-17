import abc
import http
import json

import requests
from urllib.parse import urljoin

from settings import Settings


class AbstractEsLoader:
    @abc.abstractmethod
    def set_index_schema(self, mapping_path, name):
        pass

    @abc.abstractmethod
    def load_index_data(self, data, name):
        pass


class ESLoader(AbstractEsLoader):

    def set_index_schema(self, mapping_path, name):
        f = open(mapping_path)
        body = json.dumps(json.load(f))
        response = requests.put(
            urljoin(Settings().elastic_conn.es_uri, name),
            data=body,
            headers={'Content-Type': 'application/x-ndjson'},
            verify=False,
            timeout=10
        )
        if response.status_code != http.HTTPStatus.OK:
            raise Exception('es schema is not set')

    def load_index_data(self, data, name, trasformer):
        if not data:
            return

        transformed_data = []
        for row in data:
            transformed_data.append(trasformer(row))  # TransformerUtil.transform_genre(row)

        prepared_query = []
        for row in transformed_data:
            prepared_query.extend([
                json.dumps({'index': {'_index': name, '_id': row['id']}}),
                json.dumps(row)
            ])
        str_query = '\n'.join(prepared_query) + '\n'

        response = requests.post(
            urljoin(Settings().elastic_conn.es_uri, '_bulk'),
            data=str_query,
            headers={'Content-Type': 'application/x-ndjson'},
            verify=False,
            timeout=10
        )
        if response.status_code != http.HTTPStatus.OK:
            raise Exception('check if vpn is on')
