import sqlite3

import psycopg2
from psycopg2.extensions import AsIs


class SQLoader:
    def __init__(self, sqlite_connection, pg_connection, schema, tables, rules, excluded):
        self.sqlite_conn = sqlite_connection
        self.sqlite_conn.row_factory = sqlite3.Row
        self.pg_conn = pg_connection
        self.schema = schema
        self.tables = tables
        self.rules = rules
        self.excluded = excluded

    def normalize(self, row):
        filtered_keys = []
        filtered_row = []
        for key, value in zip(row.keys(), row):
            if key in self.excluded:
                continue
            filtered_key = self.rules[key] if key in self.rules.keys() else key
            filtered_keys.append(filtered_key)
            filtered_row.append(value)
        return filtered_keys, filtered_row

    def load_all(self):
        sqlite_cur = self.sqlite_conn.cursor()
        pg_cur = self.pg_conn.cursor()
        try:
            for table_name in self.tables:
                sqlite_cur.execute('select * from %s' % table_name)
                records = fetch_records(sqlite_cur, 50)
                for row in records:
                    filtered_keys, filtered_row = self.normalize(row)
                    statement = 'insert into {table} (%s) values %s'.format(table=('%s.%s' % (self.schema, table_name)))
                    statement = pg_cur.mogrify(statement, ((AsIs(','.join(filtered_keys))), tuple(filtered_row)))
                    pg_cur.execute(statement)
                print('%s is copied!' % table_name)
        except psycopg2.errors.UniqueViolation:
            print("Data is already copied!")
            return
        except psycopg2.ProgrammingError as err:
            print(err)
            return


def fetch_records(cursor, size):
    while True:
        results = cursor.fetchmany(size)
        if not results:
            break
        for result in results:
            yield result
