import psycopg2
from decouple import config


def select_all_users():
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM users"""
        )
        return cursor.fetchall()


def add_user(username, money):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (username, money) VALUES ('{username}', {money});""")
        return f'User {username} successfully added'


print(add_user('Jotaro', 0))
