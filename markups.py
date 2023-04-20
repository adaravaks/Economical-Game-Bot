from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(row_width=2)
to_main_menu = InlineKeyboardMarkup(row_width=1)
money_menu = InlineKeyboardMarkup(row_width=2)
shop_menu = InlineKeyboardMarkup(row_width=2)
to_menus = InlineKeyboardMarkup(row_width=3)

user_checkout_btn = InlineKeyboardButton(text='Хто я?', callback_data='user_checkout')
show_leaderboard_btn = InlineKeyboardButton(text='🏆 Leaderboard', callback_data='show_leaderboard')
businesses_overview_btn = InlineKeyboardButton(text='🏦 Мои бизнесы', callback_data='business_overview')

to_money_menu_btn = InlineKeyboardButton(text='💰 Gambling', callback_data='to_money_menu')
to_shop_menu_btn = InlineKeyboardButton(text='💸 Shop', callback_data='to_shop_menu')
to_main_menu_btn = InlineKeyboardButton(text='⬅ Back to main menu', callback_data='to_main_menu')

free_bonus_btn = InlineKeyboardButton(text='🫴 Get free bonus', callback_data='free_bonus')
coin_flip_btn = InlineKeyboardButton(text='🪙 Play coin toss', callback_data='coin_toss_rules')

buy_kiosk_btn = InlineKeyboardButton(text='🗞 Купить киоск с газетами', callback_data='buy_kiosk')

main_menu.insert(user_checkout_btn)
main_menu.insert(businesses_overview_btn)
main_menu.insert(show_leaderboard_btn)
main_menu.insert(to_money_menu_btn)
main_menu.insert(to_shop_menu_btn)

money_menu.insert(free_bonus_btn)
money_menu.insert(coin_flip_btn)
money_menu.insert(to_main_menu_btn)

shop_menu.insert(buy_kiosk_btn)
shop_menu.insert(to_main_menu_btn)

to_main_menu.insert(to_main_menu_btn)

to_menus.insert(to_main_menu_btn)
to_menus.insert(to_money_menu_btn)
to_menus.insert(to_shop_menu_btn)
