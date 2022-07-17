from contextlib import contextmanager

from functools import wraps

import psycopg2
from psycopg2.extras import DictCursor
from extractor import PostgresExtractor
from storage import JsonFileStorage, State
from loader import ESLoader
from settings import Settings
import time
import logging
from time import sleep
from postman_tests_runner import run_postman_tests
import datetime
from sql_requests import *

from transformer import TransformerUtil

logger = logging.getLogger()


def etl(pg_conn, state):
    extractor = PostgresExtractor(pg_conn, state)
    loader = ESLoader()
    if not state.get_state('es_schema', None):
        loader.set_index_schema('./mappings/search_schema.json', 'movies')
        loader.set_index_schema('./mappings/genres_schema.json', 'genres')
        loader.set_index_schema('./mappings/persons_schema.json', 'persons')
        state.set_state('es_schema', True)
    last_index_time = state.get_state('last_index_time', '1970-06-16 20:14:09.221855+03')
    loader.load_index_data(extractor.extract_query(query_film_work, last_index_time), 'movies', lambda row : TransformerUtil.transform_film_work(row))
    loader.load_index_data(extractor.extract_query(query_genre, last_index_time), 'genres', lambda row : TransformerUtil.transform_genre(row))
    loader.load_index_data(extractor.extract_query(query_person, last_index_time), 'persons', lambda row : TransformerUtil.transform_person(row))
    state.set_state('last_index_time', str(datetime.datetime.utcnow() - datetime.timedelta(seconds=1)))


@contextmanager
def conn_context(pg_dsl):
    pg_conn = psycopg2.connect(**pg_dsl, cursor_factory=DictCursor)
    pg_conn.autocommit = True
    yield pg_conn
    pg_conn.close()


def retry(exception_to_check, delay=3, backoff=2):
    def deco_retry(func):
        @wraps(func)
        def f_retry(*args, **kwargs):
            m_delay = delay
            while True:
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), m_delay)
                    logger.error(msg)
                    time.sleep(m_delay)
                    m_delay *= backoff

        return f_retry

    return deco_retry

@retry(Exception, delay=2, backoff=2)
def run():
    settings = Settings()
    with psycopg2.connect(**settings.postgres_conn.dict()) as pg_conn:
        storage = JsonFileStorage(settings.etl_state.state_file)
        state = State(storage)
        etl(pg_conn, state)
        time.sleep(3)
        run_postman_tests(state)
        while True:
            etl(pg_conn, state)
            print('is running...')
            sleep(3)


if __name__ == "__main__":
    run()
