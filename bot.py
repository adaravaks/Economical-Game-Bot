from decouple import config
from random import randint, choice
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
        await message.answer('Я добавил тебя в базу данных. Не возражаешь, ведь? Вот и отлично!')
    else:
        await message.answer(f'Ты уже есть в базе данных')

    await message.answer(f'Добро пожаловать в игру, {username}', reply_markup=markups.main_menu)


@dp.message_handler(commands='menu')
async def start(message: types.Message):
    username = message.from_user.username
    await message.answer(f'😚 Привет, пупсик {username}! Вот сегодняшнее меню:',
                         reply_markup=markups.main_menu)


@dp.message_handler(commands='coin_toss')
async def coin_toss(message: types.Message):
    username = message.from_user.username
    msg_words = message.text.split()
    try:
        stake_money = int(msg_words[-1])
        if stake_money > get_user_money(username):
            await message.reply(
                f"❌ Извини, но денег тебе на такую ставку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции")
            return None  # Read as "break"

        if len(msg_words) == 3 and (msg_words[1] == 'орёл' or msg_words[1] == 'решка'):
            stake_outcome = msg_words[1]
            outcome = "орёл" if randint(0, 1) == 0 else "решка"
            if stake_outcome == outcome:
                change_money(username, stake_money)
                await message.reply(
                    f"🥳 Ура, победа! Исход падения монеты — {outcome}. В твоём кошельке внезапно оказались дополнительные {stake_money}💵.\nЕсли уверен, что удача тебя не подведёт, можешь подбросить монету ещё разок.",
                    reply_markup=markups.to_menus)
            else:
                change_money(username, -stake_money)
                await message.reply(
                    f"😰 Какая досада! Исход падения монеты — {outcome}. Твои {stake_money}💵 внезапно пропали из кошелька.\nМожет, получится отыграться, если подбросить монету ещё разок, хотя, с другой стороны, можно проиграть ещё больше. Выбор за тобой.",
                    reply_markup=markups.to_menus)
        else:
            await message.reply(
                f'С твоей командой что-то не так. Вот как её надо вводить:\n/coin_toss <орёл/решка> <твоя ставка>\nНапример:\n/coin_toss {"орёл" if randint(0, 1) == 0 else "решка"} {randint(100, 10000)}',
                reply_markup=markups.to_menus)
    except:
        await message.reply(
            f'С твоей командой что-то не так. Вот как её надо вводить:\n/coin_toss <орёл/решка> <твоя ставка>\nНапример:\n/coin_toss {"орёл" if randint(0, 1) == 0 else "решка"} {randint(100, 10000)}',
            reply_markup=markups.to_menus)


@dp.message_handler()
async def other(message: types.Message):
    await message.reply(
        'Я изо всех сил пытаюсь тебя понять, но не могу.\n😓 Пожалуйста, хватит выставлять меня дураком. Просто отправь "/menu" или нажми кнопку ниже и играй в игру, которую я для тебя приготовил.',
        reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='user_checkout')
async def user_checkout(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    username = message.from_user.username
    await bot.send_message(message.from_user.id,
                           f'👤 Имя пользователя:\n    🔹 {username}\n\n💰 Деньги:\n    🔹 {get_user_money(username)} 💵\n\n🏆 Позиция в списке богачей:\n    🔹 {user_in_leaderboard(username)}\n\n😼 Становись лучше.',
                           reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='to_main_menu')
async def back_to_menu(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    username = message.from_user.username
    await bot.send_message(message.from_user.id, f'😚 Привет, пупсик {username}! Вот сегодняшнее меню:',
                           reply_markup=markups.main_menu)


@dp.callback_query_handler(text='show_leaderboard')
async def show_leaderboard(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    leaderboard = get_leaderboard()
    str_leaderboard = '💎 Самые богатые игроки 💎\n\n'
    for player_index in range(len(leaderboard[:10])):
        str_leaderboard += f'{player_index + 1}. {leaderboard[player_index][1]}: {leaderboard[player_index][2]} 💵\n'  # Leaderboard position, then username, then user's money
    str_leaderboard += '\n😼 Лишь самые упорные, предприимчивые и везучие смогут стать частью этого списка'
    await bot.send_message(message.from_user.id, str_leaderboard, reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='to_money_menu')
async def to_money_menu(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, '🎰 Хочешь ощутить настоящий азарт и заработать небывалые деньги, а не ждать копейки дохода от предприятий? Тогда ты по адресу!🤩💰\n\n😉 Но учти, что разориться здесь также легко, как и разбогатеть.', reply_markup=markups.gambling_menu)


@dp.callback_query_handler(text='free_bonus')
async def free_bonus(message: types.Message):
    username = message.from_user.username
    if bonus_available(username):
        change_money(username, 2000)
        await bot.send_message(message.from_user.id,
                               '✅ Ты получил бонус размером в 2000 💵, поздравляю! Приходи ещё за одним через два часа😉')
    else:
        await bot.send_message(message.from_user.id,
                               "❌ Недавно ты уже получал бонус, не наглей! Новый бонус можно будет получить через два часа с момента получения предыдущего.")


@dp.callback_query_handler(text='coin_toss_rules')
async def coin_toss_rules(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'🪙 Бросок монеты, значит? Отличный выбор! Вот правила:\nЧтобы подбросить монету, вам нужно ввести команду "/coin_toss", дописать к ней исход броска (орёл/решка) и сумму вашей ставки, а затем отправить в чат. Вот пример того, как должна выглядеть команда:\n\n/coin_toss {"орёл" if randint(0, 1) == 0 else "решка"} {randint(100, 10000)}\n\nПомни, что нельзя ставить больше денег, чем у тебя есть. 😉')


@dp.callback_query_handler(text='to_shop_menu')
async def shop_menu(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, '🏦 Хочешь инвестировать деньги во что-то стабильное и получать регулярную прибыль, а не прожигать жизнь и кошелёк в мутном казино? Тогда ты по адресу!\n\n📈 Предприятие — постоянный источник пассивного дохода и разумный выбор зрелого человека.',
                           reply_markup=markups.shop_menu)


@dp.callback_query_handler(text='buy_kiosk')
async def buy_kiosk(message: types.Message):
    username = message.from_user.username
    business_func_name = 'киоск_с_газетами'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ Извини, но денег тебе на такую покупку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции 😉")
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
    await bot.delete_message(message.from_user.id, message.message.message_id)
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


@dp.callback_query_handler(text='roulette_rules')
async def roulette_rules(message: types.Message):
    example_stakes = ["красное", "чёрное", "чётное", "нечётное", "1-18", "19-36", "1-12", "13-24", "25-36", *range(37)]
    await bot.send_message(message.from_user.id,
                           f'🔴⚫ Рулетка — обязательная часть любого казино. Крутанём её разочек? Вот правила:\n\nЧтобы сыграть в рулетку, вам нужно ввести команду "/roulette", дописать к ней сектор, на который вы ставите и сумму вашей ставки, а затем отправить в чат. Допустимые сектора для ставки: "красное", "чёрное", "чётное", "нечётное", "1-18", "19-36", "1-12", "13-24", "25-36", одно любое число от 0 до 36.\nВот пример того, как должна выглядеть команда:\n\n/roulette {choice(example_stakes)} {randint(100, 10000)}\n\nПомни, что нельзя ставить больше денег, чем у тебя есть. 😉')


if __name__ == '__main__':
    executor.start_polling(dp)
