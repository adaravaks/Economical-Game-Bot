from decouple import config
from aiogram import Bot, Dispatcher, executor, types
import psycopg2


try:
    connection = psycopg2.connect(
        host=config('HOST'),
        user=config('USER'),
        password=config('PASSWORD'),
        database=config('DB_NAME')
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT version();'
        )
        print(f'current ver: {cursor.fetchone()}')

    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT username, money FROM users WHERE id = 1;"""
        )
        print([i for i in cursor.fetchone()])

except Exception as ex:
    print(f'Error has occurred: {ex}')
finally:
    if connection:
        connection.close()
        print('Connection closed')


bot = Bot(token=config('TOKEN'))
dp = Dispatcher(bot=bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
