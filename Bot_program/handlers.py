import json

from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart
import keyboards
import run as game
from Levenshtein import distance
import countries as countries
import texts as texts
from math import sqrt
from geopy.distance import geodesic
import all_russian_cities as all_russian_cities


# running = 'no' - no games running
# running = 'russian_cities' - russian cities mode running
# running = 'countries'

class UserStatus:
    def __init__(self):
        self.running = 'no'
        self.russian_cities = ''
        self.countries = ''
        self.coords = ''


USERS = {}
dp = Dispatcher()


# Handler for "/start" command
# It will send message with start_keyboard
@dp.message(CommandStart())
async def process_start_command(message: Message):
    USERS[message.from_user.id] = UserStatus()
    await message.answer(
        text=texts.hello,
        reply_markup=keyboards.start_keyboard
    )


# Handler for play button
# It will send message with mode_choice_keyboard
@dp.callback_query(F.data == 'play_button_pressed')
async def process_play_button_press(callback: CallbackQuery):
    await callback.message.answer(
        text=texts.choose,
        reply_markup=keyboards.mode_choice_keyboard
    )


# Handler for support button
# It will send message with support_keyboard
@dp.callback_query(F.data == 'support_button_pressed')
async def process_support_button_press(callback: CallbackQuery):
    await callback.message.answer(
        text=texts.to_support,
        reply_markup=keyboards.support_keyboard
    )


# Handler for info button
# It will send message with info_keyboard
@dp.callback_query(F.data == 'info_button_pressed')
async def process_info_button_press(callback: CallbackQuery):
    await callback.message.answer(
        text=texts.rules,
        reply_markup=keyboards.info_keyboard
    )


# Handler for menu button
# It will send message with start_keyboard
@dp.callback_query(F.data == 'menu_button_pressed')
async def process_menu_button_press(callback: CallbackQuery):
    await callback.message.answer(
        text=texts.hello,
        reply_markup=keyboards.start_keyboard
    )


# Handler for russian cities mode button
# It will start russian cities mode
@dp.callback_query(F.data == 'russian_cities_mode_button_pressed')
async def process_russian_cities_mode_button_press(callback: CallbackQuery):
    links, city, coords = game.run_cities()
    USERS[callback.from_user.id].running = 'russian_cities'
    USERS[callback.from_user.id].russian_cities = city
    USERS[callback.from_user.id].coords = coords
    message_data = [
        InputMediaPhoto(media=links[0], caption=texts.city_helper),
        InputMediaPhoto(media=links[1]),
        InputMediaPhoto(media=links[2]),
        InputMediaPhoto(media=links[3]),
        InputMediaPhoto(media=links[4])
    ]
    await callback.message.answer_media_group(
        media=message_data
    )


# Handler for countries mode button
# It will start countries mode
@dp.callback_query(F.data == 'countries_mode_button_pressed')
async def process_countries_mode_button_press(callback: CallbackQuery):
    links, country = game.run_countries()
    USERS[callback.from_user.id].running = 'countries'
    USERS[callback.from_user.id].countries = country
    message_data = [
        InputMediaPhoto(media=links[0], caption=texts.country_helper),
        InputMediaPhoto(media=links[1]),
        InputMediaPhoto(media=links[2]),
        InputMediaPhoto(media=links[3]),
        InputMediaPhoto(media=links[4])
    ]
    await callback.message.answer_media_group(
        media=message_data
    )


# Handler for /stop command
# It will send message with start_keyboard
@dp.message(lambda message: (message.text == '/stop' and USERS[message.from_user.id].running != 'no'))
async def process_stop_command(message: Message):
    USERS[message.from_user.id].running = 'no'
    await message.answer(
        text=texts.choose,
        reply_markup=keyboards.mode_choice_keyboard
    )


# Handler for /next command
# It will start new round of game
@dp.message(lambda message: (message.text == '/next' and USERS[message.from_user.id].running != 'no'))
async def process_next_command(message: Message):
    if USERS[message.from_user.id].running == 'russian_cities':
        links, city, coords = game.run_cities()
        USERS[message.from_user.id].russian_cities = city
        USERS[message.from_user.id].coords = coords
        message_data = [
            InputMediaPhoto(media=links[0], caption=texts.city_helper),
            InputMediaPhoto(media=links[1]),
            InputMediaPhoto(media=links[2]),
            InputMediaPhoto(media=links[3]),
            InputMediaPhoto(media=links[4])
        ]
        await message.answer_media_group(
            media=message_data
        )
    else:
        links, country = game.run_countries()
        USERS[message.from_user.id].countries = country
        message_data = [
            InputMediaPhoto(media=links[0], caption=texts.country_helper),
            InputMediaPhoto(media=links[1]),
            InputMediaPhoto(media=links[2]),
            InputMediaPhoto(media=links[3]),
            InputMediaPhoto(media=links[4])
        ]
        await message.answer_media_group(
            media=message_data
        )


# Handler for countries answers
@dp.message(lambda message: (USERS[message.from_user.id].running == 'russian_cities'))
async def process_countries_game_answer(message: Message):
    correct_answer = USERS[message.from_user.id].russian_cities
    coords = USERS[message.from_user.id].coords
    user_answer = message.text
    points = 0

    levenshtein_threshold = 3

    correct = f'Правильно! Это {correct_answer}. Вы получаете 1000 очков\nДля нового раунда игры напишите ' \
              f'/next. Если хотите закончить, напишите /stop'

    if distance(correct_answer.lower(), user_answer.lower()) <= levenshtein_threshold:
        await message.answer(
            text=correct,
        )
    else:
        if user_answer.lower() in list(all_russian_cities.all_cities.keys()):
            true_coords = all_russian_cities.all_cities[user_answer.lower()]
            d = geodesic(coords, true_coords).kilometers
            points = round(1000 / (max(sqrt(d) - 8.8, 1)))
            incorrect = f'Неправильно. Это {correct_answer}. Вы получаете {points} очков\nДля нового раунда игры ' \
                        f'напишите /next. Если хотите закончить, напишите /stop'
            await message.answer(
                text=incorrect,
            )


# Handler for cities answers
@dp.message(lambda message: (USERS[message.from_user.id].running == 'countries'))
async def process_countries_game_answer(message: Message):
    correct_answer = USERS[message.from_user.id].countries
    user_answer = message.text

    levenshtein_threshold = 3

    correct = f'Правильно! Это {correct_answer}\nДля нового раунда игры напишите /next. Если хотите закончить, ' \
              f'напишите /stop'
    incorrect = f'Неправильно. Это {correct_answer}\nДля нового раунда игры напишите /next. Если хотите закончить, ' \
                f'напишите /stop'

    if distance(correct_answer.lower(), user_answer.lower()) <= levenshtein_threshold:
        await message.answer(
            text=correct,
        )
    else:
        flag = True
        for el in countries.available_countries[correct_answer]:
            if distance(el.lower(), user_answer.lower()) <= levenshtein_threshold:
                await message.answer(
                    text=correct,
                )
                flag = False
                break
        if flag:
            await message.answer(
                text=incorrect,
            )
