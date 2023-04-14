import psycopg2
from decouple import config
from datetime import datetime


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


def get_user_money(username):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT money FROM users WHERE username='{username}'""")
        return cursor.fetchone()[0]  # fetchone() returns an one-element-long tuple, which I have no need in, so I just select that one and only element


def get_leaderboard():
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM users ORDER BY money DESC LIMIT 10""")
        return cursor.fetchall()


def user_in_leaderboard(username):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM users ORDER BY money DESC""")
        leaderboard = cursor.fetchall()

    leaderboard_dict = {}
    for index in range(len(leaderboard)):
        leaderboard_dict[leaderboard[index][1]] = index + 1  # Key is username, value is current leaderboard position

    try:
        return leaderboard_dict[username]
    except KeyError:
        return None


def bonus_available(username):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT bonus_claim_time FROM users WHERE username='{username}'""")
        last_claim_datetime = cursor.fetchone()
        if not last_claim_datetime:
            return False  # cursor.fetchone() returns empty tuple in case if there is nobody found in database with certain username, so no bonus should be given for that nobody

    try:
        timestamp_claim = datetime.strptime(str(last_claim_datetime[0]), '%Y-%m-%d %H:%M:%S.%f')
        timestamp_now = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
        delta = timestamp_now - timestamp_claim
    except ValueError:
        return True  # ValueError here raises only if user's "bonus_claim_time" in database is NULL, which means this is their first time collecting the bonus, thus they are allowed to get it

    if delta.total_seconds() >= 7200:
        return True
    return False


def add_bonus(username):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT money FROM users WHERE username='{username}'""")
        curr_money = cursor.fetchone()[0]  # Same as line 48

    with connection.cursor() as cursor:
        cursor.execute(f"""UPDATE users SET money={curr_money + 2000} WHERE username='{username}'""")
        cursor.execute(f"""UPDATE users SET bonus_claim_time='{datetime.now()}' WHERE username='{username}'""")
    return 'Bonus added successfully'
