import os

import psycopg2
from functools import wraps


def db_connection(func):
    @wraps(func)
    def with_connection(*args, **kwargs):
        connection = None
        try:
            print(os.getenv('DB_NAME'))
            connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port="5432"
            )
            cursor = connection.cursor()
            result = func(cursor, *args, **kwargs)
            connection.commit()
            return result
        except psycopg2.Error as e:
            if connection:
                connection.rollback()
            print(f"Błąd przy wykonywaniu zapytania: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    return with_connection


@db_connection
def fetch_data(cursor, query, params=None):
    cursor.execute(query, params)
    return cursor.fetchall()


@db_connection
def execute_query(cursor, query, params=None):
    cursor.execute(query, params)