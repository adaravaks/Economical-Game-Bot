from decouple import config
from aiogram import Bot, Dispatcher, executor, types
import psycopg2
from database_handler import add_user, user_exists, user_money


bot = Bot(token=config('TOKEN'))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    username = message.from_user.username
    if not user_exists(username):
        add_user(username, money=0)
        await message.answer('You were added to the database')
    else:
        await message.answer(f'You are already in the database. You are {username} and you have got {user_money(username)} money units')

    await message.answer(f'Welcome to the game, {username}')


@dp.message_handler()
async def other(message: types.Message):
    await message.reply('ок')

if __name__ == '__main__':
    executor.start_polling(dp)
