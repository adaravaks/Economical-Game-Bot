import psycopg2
from decouple import config
from datetime import datetime, timedelta


def add_user(username, money):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO users (username, money) VALUES ('{username}', {money});""")
        return f'User {username} was successfully added'


def add_business(name, func_name, price, hour_profit):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO businesses (name, func_name, price, hour_profit) VALUES ('{name}', '{func_name}', {price}, {hour_profit});""")
        return f'Business {name} was successfully added'


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


def change_money(username, money):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT money FROM users WHERE username='{username}'""")
        curr_money = cursor.fetchone()[0]

    with connection.cursor() as cursor:
        cursor.execute(f"""UPDATE users SET money={curr_money + money} WHERE username='{username}'""")
        cursor.execute(f"""UPDATE users SET bonus_claim_time='{datetime.now()}' WHERE username='{username}'""")
    return 'Money changed successfully'


def buy_business(username, business_func_name):  # TODO: It has to be made sure that user has enough money for a purchase BEFORE calling this function
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT price FROM businesses WHERE func_name='{business_func_name}'""")
        business_price = cursor.fetchone()[0]
        cursor.execute(f"""SELECT money FROM users WHERE username='{username}'""")
        user_money = cursor.fetchone()[0]
        new_user_money = user_money - business_price
        cursor.execute(f"""UPDATE users SET money={new_user_money} WHERE username='{username}'""")
        cursor.execute(f"""SELECT profit_claim_time FROM users WHERE username='{username}'""")
        if not cursor.fetchone()[0]:
            cursor.execute(f"""UPDATE users SET profit_claim_time='{datetime.now()}' WHERE username='{username}'""")

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT id FROM users WHERE username='{username}'""")
        user_id = cursor.fetchone()[0]
        cursor.execute(f"""SELECT id FROM businesses WHERE func_name='{business_func_name}'""")
        business_id = cursor.fetchone()[0]
        cursor.execute(f"""INSERT INTO users_to_businesses (user_id, business_id) VALUES ({user_id}, {business_id});""")
        return 'Business bought successfully'


def get_business_price(business_func_name):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT price FROM businesses WHERE func_name='{business_func_name}'""")
        return cursor.fetchone()[0]


def get_business_name_by_id(business_id):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT name FROM businesses WHERE id='{business_id}'""")
        return cursor.fetchone()[0]


def get_business_price_and_profit_by_funcname(business_funcname):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        lst = []
        cursor.execute(f"""SELECT price FROM businesses WHERE func_name='{business_funcname}'""")
        lst.append(cursor.fetchone()[0])
        cursor.execute(f"""SELECT hour_profit FROM businesses WHERE func_name='{business_funcname}'""")
        lst.append(cursor.fetchone()[0])
        return lst


def get_user_businesses(username):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT id FROM users WHERE username='{username}'""")
        user_id = cursor.fetchone()[0]
        cursor.execute(f"""SELECT * FROM users_to_businesses WHERE user_id='{user_id}'""")

        businesses_raw = cursor.fetchall()
        businesses_ids = [i[2] for i in businesses_raw]

        businesses_dict = {}
        for distinct_business_id in set(businesses_ids):
            businesses_dict[get_business_name_by_id(distinct_business_id)] = businesses_ids.count(distinct_business_id)
        return businesses_dict


def check_business_profit(username):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT profit_claim_time FROM users WHERE username='{username}'""")
        timestamp_claim = datetime.strptime(str(cursor.fetchone()[0]), '%Y-%m-%d %H:%M:%S.%f')
        timestamp_now = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
        hours_passed = (timestamp_now - timestamp_claim).total_seconds() // 3600

    businesses = get_user_businesses(username)
    total_profit = 0
    with connection.cursor() as cursor:
        for business_name in businesses.keys():
            cursor.execute(f"""SELECT hour_profit FROM businesses WHERE name='{business_name}'""")
            hour_profit = cursor.fetchone()[0]
            quantity = businesses[business_name]
            total_profit += quantity * hour_profit * hours_passed
    return total_profit


def receive_business_profit(username):
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT profit_claim_time FROM users WHERE username='{username}'""")
        timestamp_claim = datetime.strptime(str(cursor.fetchone()[0]), '%Y-%m-%d %H:%M:%S.%f')
        timestamp_now = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
        hours_passed = (timestamp_now - timestamp_claim).total_seconds() // 3600
        timestamp_new_claim = timestamp_claim + timedelta(hours=hours_passed)

    businesses = get_user_businesses(username)
    total_profit = 0
    with connection.cursor() as cursor:
        for business_name in businesses.keys():
            cursor.execute(f"""SELECT hour_profit FROM businesses WHERE name='{business_name}'""")
            hour_profit = cursor.fetchone()[0]
            quantity = businesses[business_name]
            total_profit += quantity * hour_profit * hours_passed

    new_money = int(get_user_money(username) + total_profit)
    with connection.cursor() as cursor:
        cursor.execute(f"""UPDATE users SET money='{new_money}' WHERE username='{username}'""")
        cursor.execute(f"""UPDATE users SET profit_claim_time='{timestamp_new_claim}' WHERE username='{username}'""")
        return 'Profit received'
