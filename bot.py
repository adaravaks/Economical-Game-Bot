from decouple import config
from time import sleep
from random import randint, choice
from aiogram import Bot, Dispatcher, executor, types
from database_handler import add_user, user_exists, get_user_money, get_leaderboard, user_in_leaderboard, \
    bonus_available, change_money, get_business_price, buy_business, get_user_businesses, check_business_profit, \
    receive_business_profit, get_business_price_and_profit_by_funcname, calculate_business_profit
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
        if len(msg_words) == 3 and (msg_words[1] == 'орёл' or msg_words[1] == 'решка'):
            if stake_money > get_user_money(username):
                await message.reply(
                    f"❌ Извини, но денег тебе на такую ставку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции")
                return None  # Read as "break"

            stake_outcome = msg_words[1]
            outcome = "орёл" if randint(0, 1) == 0 else "решка"
            if stake_outcome == outcome:
                change_money(username, stake_money)
                await message.reply(
                    f"🥳 Ура, победа!\n\nИсход падения монеты — {outcome}.\n\nВ твоём кошельке внезапно оказались дополнительные {stake_money} 💵.\nЕсли уверен, что удача тебя не подведёт, можешь подбросить монету ещё разок.",
                    reply_markup=markups.to_menus)
            else:
                change_money(username, -stake_money)
                await message.reply(
                    f"😰 Какая досада!\n\nИсход падения монеты — {outcome}.\n\nТвои {stake_money} 💵 внезапно пропали из кошелька.\nМожет, получится отыграться, если подбросить монету ещё разок, хотя, с другой стороны, можно проиграть ещё больше. Выбор за тобой.",
                    reply_markup=markups.to_menus)
        else:
            await message.reply(
                f'С твоей командой что-то не так. Вот как её надо вводить:\n/coin_toss <орёл/решка> <твоя ставка>\n\nНапример:\n/coin_toss {"орёл" if randint(0, 1) == 0 else "решка"} {randint(100, 10000)}',
                reply_markup=markups.to_menus)
    except:
        await message.reply(
            f'С твоей командой что-то не так. Вот как её надо вводить:\n/coin_toss <орёл/решка> <твоя ставка>\n\nНапример:\n/coin_toss {"орёл" if randint(0, 1) == 0 else "решка"} {randint(100, 10000)}',
            reply_markup=markups.to_menus)


@dp.message_handler(commands='roulette')
async def roulette(message: types.Message):
    username = message.from_user.username
    msg_words = message.text.split()
    possible_outcomes = ["красное", "чёрное", "чётное", "нечётное", "1-18", "19-36", "1-12", "13-24", "25-36"] + [str(i) for i in range(37)]
    try:
        stake_money = int(msg_words[-1])
        if len(msg_words) == 3 and (msg_words[1] in possible_outcomes):
            if stake_money > get_user_money(username):
                await message.reply(
                    f"❌ Извини, но денег тебе на такую ставку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции")
                return None

            stake_outcome = msg_words[1]
            outcome_number = randint(0, 36)

            outcome_color = 'красное' if outcome_number % 2 != 0 else 'чёрное'
            outcome_emoji = '🔴' if outcome_number % 2 != 0 else '⚫'
            outcome_oddeven = 'чётное' if outcome_number % 2 == 0 else 'нечётное'
            if outcome_number == 0:
                outcome_color = 'зелёное'
                outcome_emoji = '🟢'

            if outcome_number in range(1, 19):
                outcome_half = '1-18'
            elif outcome_number in range(19, 37):
                outcome_half = '19-36'
            else:
                outcome_half = None

            if outcome_number in range(1, 13):
                outcome_third = '1-12'
            elif outcome_number in range(13, 25):
                outcome_third = '13-24'
            elif outcome_number in range(25, 37):
                outcome_third = '25-36'
            else:
                outcome_third = None

            outcome = 'Win'
            if stake_outcome == outcome_color or stake_outcome == outcome_oddeven or stake_outcome == outcome_half:
                money_multiplier = 2
            elif stake_outcome == outcome_third:
                money_multiplier = 3
            elif stake_outcome == str(outcome_number):
                money_multiplier = 36
            else:
                outcome = 'Loss'
                money_multiplier = -1

            new_money = stake_money * money_multiplier
            change_money(username, new_money)
            if outcome == 'Win':
                await message.reply(
                    f'🥳 Ура, победа!\n\n Шарик рулетки упал на:\n{outcome_emoji}  {outcome_number},  {outcome_oddeven}\n\nТы выиграл, поставив на {stake_outcome}, поэтому твоя ставка возвращается к тебе в {str(money_multiplier)+"-х" if money_multiplier != 36 else str(money_multiplier)+"-и"} кратном размере.\nВ твоём кошельке внезапно оказались дополнительные {(stake_money * money_multiplier) - stake_money} 💵.\nЕсли уверен, что удача тебя не подведёт, можешь сыграть в рулетку ещё разок.',
                    reply_markup=markups.to_menus)
            else:
                await message.reply(
                    f"😰 Какая досада!\n\n Шарик рулетки упал на:\n{outcome_emoji} {outcome_number}, {outcome_oddeven}\n\nТвои {stake_money} 💵 внезапно пропали из кошелька.\nМожет, получится отыграться, если сыграть в рулетку ещё разок, хотя, с другой стороны, можно проиграть ещё больше. Выбор за тобой.",
                    reply_markup=markups.to_menus)
        else:
            await message.reply(
                f'С твоей командой что-то не так. Вот как её надо вводить:\n/roulette <сектор ставки> <сумма ставки>\n\nНапример:\n/roulette {choice(possible_outcomes)} {randint(100, 10000)}\n\n Допустимые сектора для ставки: "красное", "чёрное", "чётное", "нечётное", "1-18", "19-36", "1-12", "13-24", "25-36", одно любое число от 0 до 36.',
                reply_markup=markups.to_menus)
    except:
        await message.reply(
            f'С твоей командой что-то не так. Вот как её надо вводить:\n/roulette <сектор ставки> <сумма ставки>\n\nНапример:\n/roulette {choice(possible_outcomes)} {randint(100, 10000)}\n\n Допустимые сектора для ставки: "красное", "чёрное", "чётное", "нечётное", "1-18", "19-36", "1-12", "13-24", "25-36", одно любое число от 0 до 36.',
            reply_markup=markups.to_menus)


@dp.message_handler(commands='dice')
async def dice(message: types.Message):
    username = message.from_user.username
    msg_words = message.text.split()
    try:
        stake_money = int(msg_words[-1])
        if len(msg_words) == 3 and int(msg_words[1]) in range(1, 7):
            if stake_money > get_user_money(username):
                await message.reply(
                    f"❌ Извини, но денег тебе на такую ставку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции")
                return None

            stake_outcome = int(msg_words[1])
            outcome_raw = await message.answer_dice()
            outcome = outcome_raw['dice']['value']
            sleep(5)
            if stake_outcome == outcome:
                change_money(username, (5 * stake_money))
                await message.reply(
                    f"🥳 Ура, победа!\n\nИсход падения костей — {outcome}.\n\nВ твоём кошельке внезапно оказались дополнительные {5 * stake_money} 💵.\nЕсли уверен, что удача тебя не подведёт, можешь бросить кости ещё разок.",
                    reply_markup=markups.to_menus)
            else:
                change_money(username, -stake_money)
                await message.reply(
                    f"😰 Какая досада!\n\n Исход падения костей — {outcome}.\n\nТвои {stake_money} 💵 внезапно пропали из кошелька.\nМожет, получится отыграться, если бросить кости ещё разок, хотя, с другой стороны, можно проиграть ещё больше. Выбор за тобой.",
                    reply_markup=markups.to_menus)
        else:
            await message.reply(
                f'С твоей командой что-то не так. Вот как её надо вводить:\n/dice <число от 1 до 6> <твоя ставка>\n\nНапример:\n/dice {randint(1, 6)} {randint(100, 10000)}',
                reply_markup=markups.to_menus)
    except:
        await message.reply(
            f'С твоей командой что-то не так. Вот как её надо вводить:\n/dice <число от 1 до 6> <твоя ставка>\n\nНапример:\n/dice {randint(1, 6)} {randint(100, 10000)}',
            reply_markup=markups.to_menus)


@dp.message_handler(commands='darts')
async def darts(message: types.Message):
    username = message.from_user.username
    msg_words = message.text.split()
    try:
        stake_money = int(msg_words[-1])
        if len(msg_words) == 2:
            if stake_money > get_user_money(username):
                await message.reply(
                    f"❌ Извини, но денег тебе на такую ставку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции")
                return None

            outcome_raw = await message.answer_dice(emoji='🎯')
            outcome = outcome_raw['dice']['value']
            sleep(4)

            if int(outcome) == 6:
                change_money(username, (5 * stake_money))
                await message.reply(
                    f"🥳 Чётко в яблочко!.\n\nВ твоём кошельке внезапно оказались дополнительные {5 * stake_money} 💵.\nЕсли уверен, что удача тебя не подведёт, можешь бросить дротик ещё разок.",
                    reply_markup=markups.to_menus)
            else:
                change_money(username, -stake_money)
                await message.reply(
                    f"😰 Мимо цели!\n\nТвои {stake_money} 💵 внезапно пропали из кошелька.\nМожет, получится отыграться, если бросить дротик ещё разок, хотя, с другой стороны, можно проиграть ещё больше. Выбор за тобой.",
                    reply_markup=markups.to_menus)
        else:
            await message.reply(
                f'С твоей командой что-то не так. Вот как её надо вводить:\n/darts <твоя ставка>\n\nНапример:\n/darts {randint(100, 10000)}',
                reply_markup=markups.to_menus)
    except:
        await message.reply(
            f'С твоей командой что-то не так. Вот как её надо вводить:\n/darts <твоя ставка>\n\nНапример:\n/darts {randint(100, 10000)}',
            reply_markup=markups.to_menus)


@dp.message_handler(commands='soccer')
async def darts(message: types.Message):
    username = message.from_user.username
    msg_words = message.text.split()
    try:
        stake_money = int(msg_words[-1])
        if len(msg_words) == 2:
            if stake_money > get_user_money(username):
                await message.reply(
                    f"❌ Извини, но денег тебе на такую ставку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции")
                return None

            outcome_raw = await message.answer_dice(emoji='⚽')
            outcome = outcome_raw['dice']['value']
            sleep(5)

            if int(outcome) in [3, 4, 5]:
                change_money(username, (int(1.66 * stake_money)))
                await message.reply(
                    f"🥳 Гол!.\n\nВ твоём кошельке внезапно оказались дополнительные {int(1.66 * stake_money)} 💵.\nЕсли уверен, что удача тебя не подведёт, можешь пнуть мяч ещё разок.",
                    reply_markup=markups.to_menus)
            else:
                change_money(username, -stake_money)
                await message.reply(
                    f"😰 Мимо!\n\nТвои {stake_money} 💵 внезапно пропали из кошелька.\nМожет, получится отыграться, если пнуть мяч ещё разок, хотя, с другой стороны, можно проиграть ещё больше. Выбор за тобой.",
                    reply_markup=markups.to_menus)
        else:
            await message.reply(
                f'С твоей командой что-то не так. Вот как её надо вводить:\n/soccer <твоя ставка>\n\nНапример:\n/soccer {randint(100, 10000)}',
                reply_markup=markups.to_menus)
    except:
        await message.reply(
            f'С твоей командой что-то не так. Вот как её надо вводить:\n/soccer <твоя ставка>\n\nНапример:\n/soccer {randint(100, 10000)}',
            reply_markup=markups.to_menus)


@dp.message_handler(commands='dices')
async def darts(message: types.Message):
    outcome = await message.answer_dice(emoji='🏀')
    sleep(5)
    await message.answer(f'Исход — {outcome["dice"]["value"]}')


@dp.message_handler()
async def other(message: types.Message):
    await message.reply(
        'Я изо всех сил пытаюсь тебя понять, но не могу.\n😓 Пожалуйста, хватит выставлять меня дураком. Просто отправь "/menu" или нажми кнопку ниже и играй в игру, которую я приготовил.',
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
        str_leaderboard += f'🔹  {player_index + 1}. {leaderboard[player_index][1]}: {leaderboard[player_index][2]} 💵\n'  # Leaderboard position, then username, then user's money
    str_leaderboard += '\n😼 Лишь самые упорные, предприимчивые и везучие смогут стать частью этого списка'
    await bot.send_message(message.from_user.id, str_leaderboard, reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='to_gambling_menu')
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
                           f'🪙 Бросок монеты, значит? Отличный выбор! Вот правила:\n\nЧтобы подбросить монету, тебе нужно ввести команду "/coin_toss", дописать к ней исход броска (орёл/решка) и сумму твоей ставки, а затем отправить сообщение в чат.\nВот пример того, как должна выглядеть команда:\n\n/coin_toss {"орёл" if randint(0, 1) == 0 else "решка"} {randint(100, 10000)}\n\nПомни, что нельзя ставить больше денег, чем у тебя есть. 😉')


@dp.callback_query_handler(text='to_shop_menu')
async def shop_menu(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, '🏦 Хочешь инвестировать деньги во что-то стабильное и получать регулярную прибыль, а не прожигать жизнь и кошелёк в мутном казино? Тогда ты по адресу!\n\n📈 Предприятие — постоянный источник пассивного дохода и разумный выбор зрелого человека.',
                           reply_markup=markups.shop_menu)


@dp.callback_query_handler(text='check_kiosk')
async def check_kiosk(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f'🔵  🗞 Киоск с газетами — выгодное вложение, если ты ещё только в самом начале твоего пути к обогащению.\n\n  🔹 Цена: {get_business_price_and_profit_by_funcname("киоск_с_газетами")[0]} 💵\n  🔹 Прибыль: {get_business_price_and_profit_by_funcname("киоск_с_газетами")[1]} 💵 / час\n\n Купить?', reply_markup=markups.buy_kiosk)


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
        await bot.send_message(message.from_user.id, '✅ Поздравляю с покупкой киоска с газетами! 🥳')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='check_apiary')
async def check_apiary(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f'🔵  🍯 Пчелиная пасека поможет тебе заполнить карманы либо деньгами, либо мёдом — смотря что больше по душе. Но тебе ведь по душе деньги, да? 😉\n\n  🔹 Цена: {get_business_price_and_profit_by_funcname("пчелиная_пасека")[0]} 💵\n  🔹 Прибыль: {get_business_price_and_profit_by_funcname("пчелиная_пасека")[1]} 💵 / час\n\n Купить?', reply_markup=markups.buy_apiary)


@dp.callback_query_handler(text='buy_apiary')
async def buy_apiary(message: types.Message):
    username = message.from_user.username
    business_func_name = 'пчелиная_пасека'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ Извини, но денег тебе на такую покупку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции 😉")
        return None
    try:
        buy_business(username, business_func_name)
        await bot.send_message(message.from_user.id, '✅ Поздравляю с покупкой пчелиной пасеки! 🥳')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='check_carwash')
async def check_carwash(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f'🔵  🚗🧼 Автомойка помогала Уолтеру Уайту из "Во все тяжкие" отмывать деньги, заработанные при продаже метамфетамина. Нам до него ещё далеко, поэтому придётся использовать автомойку по прямому назначению. Зато никаких проблем с полицией, здорово же! 😌\n\n  🔹 Цена: {get_business_price_and_profit_by_funcname("автомойка")[0]} 💵\n  🔹 Прибыль: {get_business_price_and_profit_by_funcname("автомойка")[1]} 💵 / час\n\n Купить?', reply_markup=markups.buy_carwash)


@dp.callback_query_handler(text='buy_carwash')
async def buy_carwash(message: types.Message):
    username = message.from_user.username
    business_func_name = 'автомойка'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ Извини, но денег тебе на такую покупку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции 😉")
        return None
    try:
        buy_business(username, business_func_name)
        await bot.send_message(message.from_user.id, '✅ Поздравляю с покупкой автомойки! 🥳')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='check_cafe')
async def check_cafe(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f'🔵  🍛 Кафе — как заезженно! "Да эти кафешки уже на каждом углу стоят!" — ты, наверное, подумал. Но подумал ли ты, каким прибыльным делом может оказаться общепит, если подойти с умом? Давай так: ты купишь кафе, а я прослежу, чтобы оно приносило тебе прибыль. По рукам? 🤖🤝😎\n\n  🔹 Цена: {get_business_price_and_profit_by_funcname("кафе")[0]} 💵\n  🔹 Прибыль: {get_business_price_and_profit_by_funcname("кафе")[1]} 💵 / час\n\n Купить?', reply_markup=markups.buy_cafe)


@dp.callback_query_handler(text='buy_cafe')
async def buy_cafe(message: types.Message):
    username = message.from_user.username
    business_func_name = 'кафе'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ Извини, но денег тебе на такую покупку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции 😉")
        return None
    try:
        buy_business(username, business_func_name)
        await bot.send_message(message.from_user.id, '✅ Поздравляю с покупкой кафе! 🥳')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='check_cottages')
async def check_cottages(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f'🔵  🏘 Коттеджный посёлок в живописном месте — настоящий магнит для туристов и их кошельков. Найдём просторную лужайку где-нибудь возле красивого озера, силами гастарбайтеров построим там несколько домиков, а потом начнём грести деньги лопатой! Как тебе идея? 🤩\n\n  🔹 Цена: {get_business_price_and_profit_by_funcname("коттеджный_посёлок")[0]} 💵\n  🔹 Прибыль: {get_business_price_and_profit_by_funcname("коттеджный_посёлок")[1]} 💵 / час\n\n Купить?', reply_markup=markups.buy_cottages)


@dp.callback_query_handler(text='buy_cottages')
async def buy_cottages(message: types.Message):
    username = message.from_user.username
    business_func_name = 'коттеджный_посёлок'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ Извини, но денег тебе на такую покупку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции 😉")
        return None
    try:
        buy_business(username, business_func_name)
        await bot.send_message(message.from_user.id, '✅ Поздравляю с покупкой коттеджного посёлка! 🥳')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='check_tvshow')
async def check_tvshow(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f'🔵  📽 ТВ-шоу со звёздами будет притягивать к себе внимание уставших работяг, пришедших вечером с работы и желающих отдохнуть перед телевизором с бутылкой какой-нибудь бурды. Чем больше мы таких соберём перед экранами — тем больше денег получим от рекламных пауз. Конечно, огромные рейтинги требуют огромной зрелищности, но эту часть я готов взять на себя. Ну что, порвём экраны? 😈\n\n  🔹 Цена: {get_business_price_and_profit_by_funcname("тв_шоу_со_звёздами")[0]} 💵\n  🔹 Прибыль: {get_business_price_and_profit_by_funcname("тв_шоу_со_звёздами")[1]} 💵 / час\n\n Купить?', reply_markup=markups.buy_tvshow)


@dp.callback_query_handler(text='buy_tvshow')
async def buy_tvshow(message: types.Message):
    username = message.from_user.username
    business_func_name = 'тв_шоу_со_звёздами'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ Извини, но денег тебе на такую покупку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции 😉")
        return None
    try:
        buy_business(username, business_func_name)
        await bot.send_message(message.from_user.id, '✅ Поздравляю с запуском своего собственного ТВ-шоу! 🥳')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='check_bank')
async def check_bank(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f'🔵  🏦 Банк. Хватит ребячества, пора заняться серьёзным делом. Оседлаем этого капиталистического зверя — и сможем сосредоточить у себя капитал, которого доселе ты и во снах не видел. Ты со мной? 😏\n\n  🔹 Цена: {get_business_price_and_profit_by_funcname("банк")[0]} 💵\n  🔹 Прибыль: {get_business_price_and_profit_by_funcname("банк")[1]} 💵 / час\n\n Купить?', reply_markup=markups.buy_bank)


@dp.callback_query_handler(text='buy_bank')
async def buy_bank(message: types.Message):
    username = message.from_user.username
    business_func_name = 'банк'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ Извини, но денег тебе на такую покупку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции 😉")
        return None
    try:
        buy_business(username, business_func_name)
        await bot.send_message(message.from_user.id, '✅ Поздравляю с покупкой банка! 🥳')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='check_pmc')
async def check_pmc(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f'🔵  💣 Частная военная компания — отбрось мораль и стань ещё богаче! Война — очень прибыльное дело, ты знал об этом? Если не станешь глупить и брезговать кровавыми деньгами, то со временем перед твоим богатством откроются все двери этого мира. Готов устроить мясорубку? 👹\n\n  🔹 Цена: {get_business_price_and_profit_by_funcname("частная_военная_компания")[0]} 💵\n  🔹 Прибыль: {get_business_price_and_profit_by_funcname("частная_военная_компания")[1]} 💵 / час\n\n Купить?', reply_markup=markups.buy_pmc)


@dp.callback_query_handler(text='buy_pmc')
async def buy_pmc(message: types.Message):
    username = message.from_user.username
    business_func_name = 'частная_военная_компания'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ Извини, но денег тебе на такую покупку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции 😉")
        return None
    try:
        buy_business(username, business_func_name)
        await bot.send_message(message.from_user.id, '✅ Поздравляю с основанием ЧВК! 😈')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='check_spacecolonies')
async def check_spacecolonies(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f'🔵  🚀 Колонизация космоса станет твоим триумфальным последним шагом. Когда Земля больше не способна удовлетворить твои потребности, всё, что остаётся — отправиться за её пределы. Цена такой кампании, действительно, космическая, но потенциальная прибыль точно стоит всех твоих затрат. Дерзнёшь рвануть в космос? 🌌\n\n  🔹 Цена: {get_business_price_and_profit_by_funcname("колонизация_космоса")[0]} 💵\n  🔹 Прибыль: {get_business_price_and_profit_by_funcname("колонизация_космоса")[1]} 💵 / час\n\n Купить?', reply_markup=markups.buy_spacecolonies)


@dp.callback_query_handler(text='buy_spacecolonies')
async def buy_spacecolonies(message: types.Message):
    username = message.from_user.username
    business_func_name = 'колонизация_космоса'
    if get_user_money(username) < get_business_price(business_func_name):
        await bot.send_message(message.from_user.id,
                               "❌ Извини, но денег тебе на такую покупку не хватит. Влезать в долги тоже не вариант, так что поумерь свои амбиции 😉")
        return None
    try:
        buy_business(username, business_func_name)
        await bot.send_message(message.from_user.id, '✅ Поздравляю с началом космической экспансии! 🚀🥳\nМожешь считать, что игра пройдена:)')
    except:
        await bot.send_message(message.from_user.id, '❌ Покупка не удалась')


@dp.callback_query_handler(text='business_overview')
async def business_overview(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    username = message.from_user.username
    overview = '🤩 Вот, взгляни, чего мы уже добились:\n\n'
    businesses = get_user_businesses(username)

    if businesses:
        profits = calculate_business_profit(username)
        for business_name in businesses.keys():
            overview += f'🔵  {business_name}:\n    🔹  Количество: {businesses[business_name]}\n    🔹  Прибыль: {profits[business_name]}\n\n'
    else:
        await bot.send_message(message.from_user.id,
                               '❌ Что ты надеешься здесь увидеть, не имея ни одного предприятия?',
                               reply_markup=markups.to_main_menu)
        return None
    await bot.send_message(message.from_user.id, overview, reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='check_profit')
async def check_profit(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    username = message.from_user.username
    if not get_user_businesses(username):
        await bot.send_message(message.from_user.id,
                               '❌ Какая ещё прибыль? Ты для начала хоть одним предприятием обзаведись.',
                               reply_markup=markups.to_main_menu)
    elif sum(calculate_business_profit(username).values()) == 0:
        await bot.send_message(message.from_user.id,
                               f'❌ Твои предприятия ещё не успели ничего заработать.\nЯ, конечно, нанял самых лучших управляющих, но и они не сверхлюди. Дай им немного времени, а? 😉',
                               reply_markup=markups.to_main_menu)
    else:
        profits = calculate_business_profit(username)
        msg = f'За то время, что тебя не было, твои предприятия заработали тебе {sum(profits.values())} 💵.\nПодробнее:\n\n'
        for business_name in profits.keys():
            msg += f'🔵  {business_name}:\n    🔹  Прибыль: {profits[business_name]}\n\n'
        msg += 'Солидная сумма! Хочешь её забрать? 😉'
        await bot.send_message(message.from_user.id, msg, reply_markup=markups.receive_profit)


@dp.callback_query_handler(text='receive_profit')
async def receive_profit(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    username = message.from_user.username
    profit = check_business_profit(username)
    if not get_user_businesses(username):
        await bot.send_message(message.from_user.id,
                               '❌ Нельзя забрать прибыль от предприятий, не имея ни одного из них. На что ты вообще надеялся?',
                               reply_markup=markups.to_main_menu)
    else:
        receive_business_profit(username)
        await bot.send_message(message.from_user.id,
                               f'✅ Твой кошелёк пополнился дополнительными {profit} 💵 от управляющих вашими предприятиями, поздравляю!',
                               reply_markup=markups.to_main_menu)


@dp.callback_query_handler(text='roulette_rules')
async def roulette_rules(message: types.Message):
    example_stakes = ["красное", "чёрное", "чётное", "нечётное", "1-18", "19-36", "1-12", "13-24", "25-36", *range(37)]
    await bot.send_message(message.from_user.id,
                           f'🔴⚫ Рулетка — обязательная часть любого казино. Крутанём её разочек? Вот правила:\n\nЧтобы сыграть в рулетку, тебе нужно ввести команду "/roulette", дописать к ней сектор, на который ты ставишь и сумму твоей ставки, а затем отправить сообщение в чат. Допустимые сектора для ставки: "красное", "чёрное", "чётное", "нечётное", "1-18", "19-36", "1-12", "13-24", "25-36", одно любое число от 0 до 36.\nВот пример того, как должна выглядеть команда:\n\n/roulette {choice(example_stakes)} {randint(100, 10000)}\n\nЕсли ставка оказалась выигрышной, то сумма выигрыша рассчитывается по такой формуле: 36 / <число полей, которое покрывала твоя ставка>. Например, поставив 1000 💵 на "13-24", ты можешь выиграть 3000 💵, а поставив на "0" — 36000 💵 \n\nПомни, что нельзя ставить больше денег, чем у тебя есть. 😉')


@dp.callback_query_handler(text='dice_rules')
async def dice_rules(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'🎲 Бросок костей — основа игрового процесса множества настольных игр, но у нас тут игра не настольная, а экономическая, поэтому сделаем-ка мы лучше на эти кости ставочку:) Вот правила:\n\nЧтобы бросить кости, тебе нужно ввести команду "/dice", дописать к ней ожидаемый результат броска и твою ставку, а затем отправить сообщение в чат. У костей шесть сторон, поэтому при победе твоя ставка вернётся к тебе в шестикратном размере.\nВот пример того, как должна выглядеть команда:\n\n/dice {randint(1, 6)} {randint(100, 10000)}\n\nПомни, что нельзя ставить больше денег, чем у тебя есть. 😉')


@dp.callback_query_handler(text='darts_rules')
async def dice_rules(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'🎯 Дартс — игра на меткость, а у нас будет ещё и на деньги. Вот правила:\n\nЧтобы сыграть в дартс, тебе нужно ввести команду "/darts", дописать к ней твою ставку, а затем отправить сообщение в чат. Шанс попасть в яблочко составляет 1/6, поэтому при победе твоя ставка вернётся к тебе в шестикратном размере.\nВот пример того, как должна выглядеть команда:\n\n/darts {randint(100, 10000)}\n\nПомни, что нельзя ставить больше денег, чем у тебя есть. 😉')


@dp.callback_query_handler(text='soccer_rules')
async def dice_rules(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'⚽ Футбол — настоящий магнит для ставок. Футболистов у нас нет, зато есть ставки. Сыграем? Вот правила:\n\nЧтобы сыграть в футбол, тебе нужно ввести команду "/soccer", дописать к ней твою ставку, а затем отправить сообщение в чат. Шанс попасть в ворота составляет 3/5, поэтому при победе твоя ставка вернётся к тебе в 1.66-кратном размере.\nВот пример того, как должна выглядеть команда:\n\n/soccer {randint(100, 10000)}\n\nПомни, что нельзя ставить больше денег, чем у тебя есть. 😉')


if __name__ == '__main__':
    executor.start_polling(dp)
