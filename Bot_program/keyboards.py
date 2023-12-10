from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Buttons
info_button = InlineKeyboardButton(
    text='Инфо/правила',
    callback_data='info_button_pressed'
)

play_button = InlineKeyboardButton(
    text='Играть',
    callback_data='play_button_pressed'
)

support_button = InlineKeyboardButton(
    text='Поддержка',
    callback_data='support_button_pressed'
)

# TODO: Поменять название режимов
first_mode_button = InlineKeyboardButton(
    text='First mode',
    callback_data='first_mode_button_pressed'
)

second_mode_button = InlineKeyboardButton(
    text='Second mode',
    callback_data='second_mode_button_pressed'
)

menu_button = InlineKeyboardButton(
    text='Меню',
    callback_data='menu_button_pressed'
)

# Keyboards
start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [info_button, play_button, support_button]
    ]
)

info_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [play_button, support_button]
    ]
)

support_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [info_button, play_button]
    ]
)

mode_choice_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [first_mode_button, second_mode_button],
        [menu_button]
    ]
)
