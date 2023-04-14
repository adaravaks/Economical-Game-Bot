from decouple import config
from aiogram import Bot, Dispatcher, executor, types
from database_handler import add_user, user_exists, get_user_money, get_leaderboard, user_in_leaderboard, bonus_available, add_bonus
import markups


bot = Bot(token=config('TOKEN'))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    username = message.from_user.username
    if not user_exists(username):
        add_user(username, money=0)
        await message.answer('You were added to the database')
    else:
        await message.answer(f'You are already in the database')

    await message.answer(f'Welcome to the game, {username}', reply_markup=markups.main_menu)


@dp.message_handler()
async def other(message: types.Message):
    await message.reply('explain yourself')


@dp.callback_query_handler(text='user_checkout')
async def user_checkout(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    username = message.from_user.username
    await bot.send_message(message.from_user.id, f'Username: {username}\nMoney: {get_user_money(username)} 💵\nLeaderboard position: {user_in_leaderboard(username)}\nGet better.', reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='to_main_menu')
async def back_to_menu(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    username = message.from_user.username
    await bot.send_message(message.from_user.id, f'Welcome to the game, {username}', reply_markup=markups.main_menu)


@dp.callback_query_handler(text='show_leaderboard')
async def show_leaderboard(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)

    leaderboard = get_leaderboard()
    str_leaderboard = ''
    for player_index in range(len(leaderboard[:10])):
        str_leaderboard += f'{player_index+1}. {leaderboard[player_index][1]}: {leaderboard[player_index][2]} 💵\n'  # Leaderboard position, then username, then user's money

    await bot.send_message(message.from_user.id, str_leaderboard, reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='to_money_menu')
async def to_money_menu(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Alright, here goes business!🤩💰', reply_markup=markups.money_menu)


@dp.callback_query_handler(text='free_bonus')
async def free_bonus(message: types.Message):
    username = message.from_user.username
    if bonus_available(username):
        add_bonus(username)
        await bot.send_message(message.from_user.id, '✅ You received a bonus of 2000 money units, congrats! Come back for the new one in two hours😉')
    else:
        await bot.send_message(message.from_user.id, "❌ You have already received a bonus recently, don't be so greedy! You will be able to receive a new bonus after two hours since the moment you received the previous one.")


if __name__ == '__main__':
    executor.start_polling(dp)
