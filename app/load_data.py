import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from loader import SQLoader


def load_from_sqlite(sqlite_connection: sqlite3.Connection, pg_connection: _connection):
    # dataclass не использовал, не могу понять, что мы выиграем от их использования,
    # наоборот, показалось, что они добавят хрупкости коду
    sql_loader = SQLoader(sqlite_connection,
                          pg_connection,
                          'public',
                          ['film_work', 'genre', 'genre_film_work', 'person', 'person_film_work'],
                          {'updated_at': 'modified', 'created_at': 'created'},
                          ['file_path'])
    sql_loader.load_all()


@contextmanager
def conn_context(sqlite_path, pg_dsl):
    sqlite_conn = sqlite3.connect(sqlite_path)
    pg_conn = psycopg2.connect(**pg_dsl, cursor_factory=DictCursor)
    pg_conn.autocommit = True
    yield sqlite_conn, pg_conn
    sqlite_conn.close()
    pg_conn.close()


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': 'postgres', 'port': 5432}
    with conn_context('db.sqlite', dsl) as (sqlite_conn, pg_conn):
        load_from_sqlite(sqlite_conn, pg_conn)
