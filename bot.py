from decouple import config
from random import randint
from aiogram import Bot, Dispatcher, executor, types
from database_handler import add_user, user_exists, get_user_money, get_leaderboard, user_in_leaderboard, \
    bonus_available, change_money, get_business_price, buy_business, get_user_businesses, check_business_profit, \
    receive_business_profit
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


@dp.message_handler(commands='menu')
async def start(message: types.Message):
    username = message.from_user.username
    await message.answer(f'😚 Hi there, sweetie {username}! Here is your menu for today:',
                         reply_markup=markups.main_menu)


@dp.message_handler(commands='coin_toss')
async def coin_toss(message: types.Message):
    username = message.from_user.username
    msg_words = message.text.split()
    try:
        stake_money = int(msg_words[-1])
        if stake_money > get_user_money(username):
            await message.reply(
                f"I am sorry, but you don't have enough money to make stakes like that. Going debt is not the option either, so leash your ambitions.")
            return None  # Read as "break"

        if len(msg_words) == 3 and (msg_words[1] == 'heads' or msg_words[1] == 'tails'):
            stake_outcome = msg_words[1]
            outcome = "heads" if randint(0, 1) == 0 else "tails"
            if stake_outcome == outcome:
                change_money(username, stake_money)
                await message.reply(
                    f"🥳 Congrats, you won! The coin landed on it's {outcome} and your wallet has been expended by additional {stake_money}💵.\nYou can play coin toss one more time if you're sure your luck won't fail you.",
                    reply_markup=markups.to_menus)
            else:
                change_money(username, -stake_money)
                await message.reply(
                    f"😰 Oh no, you lost! The coin landed on it's {outcome} and your {stake_money}💵 have suddenly disappeared from your wallet.\nPerhaps, you can get your money back if you play coin toss one more time, though you can lose even more as well. The decision is up to you.",
                    reply_markup=markups.to_menus)
        else:
            await message.reply(
                f'There is something wrong with your command. This is how it should be entered:\n/coin_toss <heads/tails> <your stake>\nFor example:\n/coin_toss {"heads" if randint(0, 1) == 0 else "tails"} {randint(100, 10000)}',
                reply_markup=markups.to_menus)
    except:
        await message.reply(
            f'There is something wrong with your command. This is how it should be entered:\n/coin_toss <heads/tails> <your stake>\nFor example:\n/coin_toss {"heads" if randint(0, 1) == 0 else "tails"} {randint(100, 10000)}',
            reply_markup=markups.to_menus)


@dp.message_handler()
async def other(message: types.Message):
    await message.reply(
        'I am trying my best to understand you, but I still can not, which makes  me feel dumb.\n😓 Please, stop embarrassing me. Just use "/menu" or press the button below and play the game I prepared for you',
        reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='user_checkout')
async def user_checkout(message: types.Message):
    username = message.from_user.username
    await bot.send_message(message.from_user.id,
                           f'Username: {username}\nMoney: {get_user_money(username)} 💵\nLeaderboard position: {user_in_leaderboard(username)}\nGet better.',
                           reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='to_main_menu')
async def back_to_menu(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    username = message.from_user.username
    await bot.send_message(message.from_user.id, f'😚 Hi there, sweetie {username}! Here is your menu for today:',
                           reply_markup=markups.main_menu)


@dp.callback_query_handler(text='show_leaderboard')
async def show_leaderboard(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    leaderboard = get_leaderboard()
    str_leaderboard = ''
    for player_index in range(len(leaderboard[:10])):
        str_leaderboard += f'{player_index + 1}. {leaderboard[player_index][1]}: {leaderboard[player_index][2]} 💵\n'  # Leaderboard position, then username, then user's money

    await bot.send_message(message.from_user.id, str_leaderboard, reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='to_money_menu')
async def to_money_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Alright, here goes gambling!🤩💰', reply_markup=markups.gambling_menu)


@dp.callback_query_handler(text='free_bonus')
async def free_bonus(message: types.Message):
    username = message.from_user.username
    if bonus_available(username):
        change_money(username, 2000)
        await bot.send_message(message.from_user.id,
                               '✅ You received a bonus of 2000 💵, congrats! Come back for the new one in two hours😉')
    else:
        await bot.send_message(message.from_user.id,
                               "❌ You have already received a bonus recently, don't be so greedy! You will be able to receive a new bonus after two hours since the moment you received the previous one.")


@dp.callback_query_handler(text='coin_toss_rules')
async def coin_toss_rules(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Coin toss, huh? Very well then! Here are the rules:\nTo play coin toss, you must enter "/coin_toss" command and send it followed by the outcome you expect and size of your stake. This is the example of how it should look:\n\n/coin_toss {"heads" if randint(0, 1) == 0 else "tails"} {randint(100, 10000)}\n\nRemember, that you can not bet more money than you have in your wallet 😉')


@dp.callback_query_handler(text='to_shop_menu')
async def shop_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'Wanna invest your money in something? Sure! Here go businesses! 📈',
                           reply_markup=markups.shop_menu)


@dp.callback_query_handler(text='buy_kiosk')
async def buy_kiosk(message: types.Message):
    username = message.from_user.username
    business_func_name = 'киоск_с_газетами'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ I am sorry, but you don't have enough money to make purchases like that. Going debt is not the option either, so leash your ambitions.")
        return None
    try:
        buy_business(username, business_func_name)
        await bot.send_message(message.from_user.id, '✅ Поздравляю с покупкой киоска с газетами')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='business_overview')
async def business_overview(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    username = message.from_user.username
    overview = ''
    businesses = get_user_businesses(username)

    for business_name in businesses.keys():
        overview += f'{business_name}: {businesses[business_name]}\n'
    await bot.send_message(message.from_user.id, overview, reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='check_profit')
async def check_profit(message: types.Message):
    username = message.from_user.username
    if not get_user_businesses(username):
        await bot.send_message(message.from_user.id,
                               '❌ Да у тебя ведь ни одного предприятия нет, что это ты забрать удумал?',
                               reply_markup=markups.to_main_menu)
    else:
        await bot.send_message(message.from_user.id,
                               f'🕓 За то время, что вас не было, ваши предприятия заработали вам {check_business_profit(username)} 💵\nСолидная сумма! Хотите её забрать? 😉',
                               reply_markup=markups.receive_profit)


@dp.callback_query_handler(text='receive_profit')
async def receive_profit(message: types.Message):
    username = message.from_user.username
    profit = check_business_profit(username)
    if not get_user_businesses(username):
        await bot.send_message(message.from_user.id,
                               '❌ Нельзя забрать прибыль от предприятий, не имея ни одного из них. На что ты вообще надеялся?',
                               reply_markup=markups.to_main_menu)
    else:
        receive_business_profit(username)
        await bot.send_message(message.from_user.id,
                               f'✅ Ваш кошелёк пополнился дополнительными {profit} 💵 от управляющих вашими предприятиями, поздравляю!',
                               reply_markup=markups.to_main_menu)


if __name__ == '__main__':
    executor.start_polling(dp)
