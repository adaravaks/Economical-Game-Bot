from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(row_width=2)
back_to_menu = InlineKeyboardMarkup(row_width=1)

user_checkout_btn = InlineKeyboardButton(text='Хто я?', callback_data='user_checkout')
back_to_menu_btn = InlineKeyboardButton(text='Back to main menu', callback_data='back_to_menu')

main_menu.insert(user_checkout_btn)
back_to_menu.insert(back_to_menu_btn)
