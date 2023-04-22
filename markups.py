from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(row_width=1)
to_main_menu = InlineKeyboardMarkup(row_width=1)
gambling_menu = InlineKeyboardMarkup(row_width=1)
shop_menu = InlineKeyboardMarkup(row_width=1)
to_menus = InlineKeyboardMarkup(row_width=1)
receive_profit = InlineKeyboardMarkup(row_width=1)

buy_kiosk = InlineKeyboardMarkup(row_width=1)

user_checkout_btn = InlineKeyboardButton(text='👤 Мой профиль', callback_data='user_checkout')
show_leaderboard_btn = InlineKeyboardButton(text='🏆 Список богачей', callback_data='show_leaderboard')
businesses_overview_btn = InlineKeyboardButton(text='🏦 Мои предприятия', callback_data='business_overview')

to_gambling_menu_btn = InlineKeyboardButton(text='🎰 Азартные игры', callback_data='to_gambling_menu')
to_shop_menu_btn = InlineKeyboardButton(text='💸 Бизнес-магазин', callback_data='to_shop_menu')
to_main_menu_btn = InlineKeyboardButton(text='⬅ В главное меню', callback_data='to_main_menu')

free_bonus_btn = InlineKeyboardButton(text='🫴 Получить бесплатный бонус', callback_data='free_bonus')
coin_flip_btn = InlineKeyboardButton(text='🪙 Бросок монеты', callback_data='coin_toss_rules')
roulette_btn = InlineKeyboardButton(text='🔴⚫ Рулетка', callback_data='roulette_rules')

check_profit_btn = InlineKeyboardButton(text='💰 Прибыль от предприятий', callback_data='check_profit')
receive_profit_btn = InlineKeyboardButton(text='🤑 Забрать', callback_data='receive_profit')
check_kiosk_btn = InlineKeyboardButton(text='🗞 Киоск с газетами', callback_data='check_kiosk')
buy_kiosk_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_kiosk')

main_menu.insert(user_checkout_btn)
main_menu.insert(show_leaderboard_btn)
main_menu.insert(to_gambling_menu_btn)
main_menu.insert(to_shop_menu_btn)
main_menu.insert(businesses_overview_btn)
main_menu.insert(check_profit_btn)

gambling_menu.insert(free_bonus_btn)
gambling_menu.insert(coin_flip_btn)
gambling_menu.insert(roulette_btn)
gambling_menu.insert(to_main_menu_btn)

shop_menu.insert(check_kiosk_btn)
shop_menu.insert(to_main_menu_btn)

to_main_menu.insert(to_main_menu_btn)

to_menus.insert(to_main_menu_btn)
to_menus.insert(to_gambling_menu_btn)
to_menus.insert(to_shop_menu_btn)

receive_profit.insert(receive_profit_btn)
receive_profit.insert(to_main_menu_btn)

buy_kiosk.insert(buy_kiosk_btn)
buy_kiosk.insert(to_main_menu_btn)
