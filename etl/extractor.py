import abc

from psycopg2.extras import RealDictCursor


class AbstractExtractor:

    @abc.abstractmethod
    def extract_query(self, query, args):
        pass


class PostgresExtractor:
    last_index_time = ''

    def __init__(self, pg_conn, state):
        self.cursor = pg_conn.cursor(cursor_factory=RealDictCursor)
        self.state = state

    def extract_query(self, query, last_time):
        self.cursor.execute(query, (last_time,))
        data = self.cursor.fetchall()
        return data
