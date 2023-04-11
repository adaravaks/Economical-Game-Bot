import psycopg2
from decouple import config


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
        return f'User {username} was successfully added'


def user_exists(username):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM users WHERE username='{username}'""")
        if cursor.fetchall():
            return True
        return False


def user_money(username):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT money FROM users WHERE username='{username}'""")
        return cursor.fetchone()[0]  # fetchone() returns an one-element-long tuple, which is unnecessary for me, so I just select the element
