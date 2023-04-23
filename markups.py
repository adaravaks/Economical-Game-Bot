from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(row_width=1)
to_main_menu = InlineKeyboardMarkup(row_width=1)
gambling_menu = InlineKeyboardMarkup(row_width=1)
shop_menu = InlineKeyboardMarkup(row_width=1)
to_menus = InlineKeyboardMarkup(row_width=1)
receive_profit = InlineKeyboardMarkup(row_width=1)

buy_kiosk = InlineKeyboardMarkup(row_width=1)
buy_apiary = InlineKeyboardMarkup(row_width=1)
buy_carwash = InlineKeyboardMarkup(row_width=1)
buy_cafe = InlineKeyboardMarkup(row_width=1)
buy_cottages = InlineKeyboardMarkup(row_width=1)
buy_tvshow = InlineKeyboardMarkup(row_width=1)
buy_bank = InlineKeyboardMarkup(row_width=1)
buy_pmc = InlineKeyboardMarkup(row_width=1)
buy_spacecolonies = InlineKeyboardMarkup(row_width=1)

user_checkout_btn = InlineKeyboardButton(text='👤 Мой профиль', callback_data='user_checkout')
show_leaderboard_btn = InlineKeyboardButton(text='🏆 Список богачей', callback_data='show_leaderboard')
businesses_overview_btn = InlineKeyboardButton(text='🏦 Мои предприятия', callback_data='business_overview')

to_gambling_menu_btn = InlineKeyboardButton(text='🎰 Азартные игры', callback_data='to_gambling_menu')
to_shop_menu_btn = InlineKeyboardButton(text='💸 Бизнес-магазин', callback_data='to_shop_menu')
to_main_menu_btn = InlineKeyboardButton(text='⬅ В главное меню', callback_data='to_main_menu')

free_bonus_btn = InlineKeyboardButton(text='🫴 Получить бесплатный бонус', callback_data='free_bonus')
coin_flip_btn = InlineKeyboardButton(text='🪙 Бросок монеты', callback_data='coin_toss_rules')
roulette_btn = InlineKeyboardButton(text='🔴⚫ Рулетка', callback_data='roulette_rules')
dice_btn = InlineKeyboardButton(text='🎲 Бросок костей', callback_data='dice_rules')

check_profit_btn = InlineKeyboardButton(text='💰 Прибыль от предприятий', callback_data='check_profit')
receive_profit_btn = InlineKeyboardButton(text='🤑 Забрать', callback_data='receive_profit')

check_kiosk_btn = InlineKeyboardButton(text='🗞 Киоск с газетами', callback_data='check_kiosk')
buy_kiosk_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_kiosk')

check_apiary_btn = InlineKeyboardButton(text='🍯 Пчелиная пасека', callback_data='check_apiary')
buy_apiary_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_apiary')

check_carwash_btn = InlineKeyboardButton(text='🚗🧼 Автомойка', callback_data='check_carwash')
buy_carwash_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_carwash')

check_cafe_btn = InlineKeyboardButton(text='🍛 Кафе', callback_data='check_cafe')
buy_cafe_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_cafe')

check_cottages_btn = InlineKeyboardButton(text='🏘 Коттеджный посёлок', callback_data='check_cottages')
buy_cottages_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_cottages')

check_tvshow_btn = InlineKeyboardButton(text='📽 ТВ-шоу со звёздами', callback_data='check_tvshow')
buy_tvshow_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_tvshow')

check_bank_btn = InlineKeyboardButton(text='🏦 Банк', callback_data='check_bank')
buy_bank_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_bank')

check_pmc_btn = InlineKeyboardButton(text='💣 Частная военная компания', callback_data='check_pmc')
buy_pmc_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_pmc')

check_spacecolonies_btn = InlineKeyboardButton(text='🚀 Колонизация космоса', callback_data='check_spacecolonies')
buy_spacecolonies_btn = InlineKeyboardButton(text='👍 Купить', callback_data='buy_spacecolonies')

main_menu.insert(user_checkout_btn)
main_menu.insert(show_leaderboard_btn)
main_menu.insert(free_bonus_btn)
main_menu.insert(to_gambling_menu_btn)
main_menu.insert(to_shop_menu_btn)
main_menu.insert(businesses_overview_btn)
main_menu.insert(check_profit_btn)

gambling_menu.insert(coin_flip_btn)
gambling_menu.insert(roulette_btn)
gambling_menu.insert(dice_btn)
gambling_menu.insert(to_main_menu_btn)

shop_menu.insert(check_kiosk_btn)
shop_menu.insert(check_apiary_btn)
shop_menu.insert(check_carwash_btn)
shop_menu.insert(check_cafe_btn)
shop_menu.insert(check_cottages_btn)
shop_menu.insert(check_tvshow_btn)
shop_menu.insert(check_bank_btn)
shop_menu.insert(check_pmc_btn)
shop_menu.insert(check_spacecolonies_btn)
shop_menu.insert(to_main_menu_btn)

to_main_menu.insert(to_main_menu_btn)

to_menus.insert(to_main_menu_btn)
to_menus.insert(to_gambling_menu_btn)
to_menus.insert(to_shop_menu_btn)

receive_profit.insert(receive_profit_btn)
receive_profit.insert(to_main_menu_btn)

buy_kiosk.insert(buy_kiosk_btn)
buy_kiosk.insert(to_shop_menu_btn)
buy_kiosk.insert(to_main_menu_btn)

buy_apiary.insert(buy_apiary_btn)
buy_apiary.insert(to_shop_menu_btn)
buy_apiary.insert(to_main_menu_btn)

buy_carwash.insert(buy_carwash_btn)
buy_carwash.insert(to_shop_menu_btn)
buy_carwash.insert(to_main_menu_btn)

buy_cafe.insert(buy_cafe_btn)
buy_cafe.insert(to_shop_menu_btn)
buy_cafe.insert(to_main_menu_btn)

buy_cottages.insert(buy_cottages_btn)
buy_cottages.insert(to_shop_menu_btn)
buy_cottages.insert(to_main_menu_btn)

buy_tvshow.insert(buy_tvshow_btn)
buy_tvshow.insert(to_shop_menu_btn)
buy_tvshow.insert(to_main_menu_btn)

buy_bank.insert(buy_bank_btn)
buy_bank.insert(to_shop_menu_btn)
buy_bank.insert(to_main_menu_btn)

buy_pmc.insert(buy_pmc_btn)
buy_pmc.insert(to_shop_menu_btn)
buy_pmc.insert(to_main_menu_btn)

buy_spacecolonies.insert(buy_spacecolonies_btn)
buy_spacecolonies.insert(to_shop_menu_btn)
buy_spacecolonies.insert(to_main_menu_btn)
