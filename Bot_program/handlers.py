from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart
import keyboards
import Game_formation.start_game as game
from Levenshtein import distance
import GeoQuest.Bot_program.synonyms as synonyms
import GeoQuest.Bot_program.texts as texts

# running = 'no' - no games running
# running = 'russian_cities' - russian cities mode running
# running = 'countries'

GAME_STATUS = {'running': 'no', 'russian_cities': '', 'countries': ''}
dp = Dispatcher()


# Handler for "/start" command
# It will send message with start_keyboard
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=texts.hello,
        reply_markup=keyboards.start_keyboard
    )


# TODO: Дописать правила
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
    links, city = game.run_cities()
    GAME_STATUS['running'] = 'russian_cities'
    GAME_STATUS['russian_cities'] = city
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
    GAME_STATUS['running'] = 'countries'
    GAME_STATUS['countries'] = country
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
@dp.message(lambda message: (message.text == '/stop' and GAME_STATUS['running'] != 'no'))
async def process_stop_command(message: Message):
    GAME_STATUS['running'] = 'no'
    await message.answer(
        text=texts.choose,
        reply_markup=keyboards.mode_choice_keyboard
    )


# Handler for /next command
# It will start new round of game
@dp.message(lambda message: (message.text == '/next' and GAME_STATUS['running'] != 'no'))
async def process_next_command(message: Message):
    if GAME_STATUS['running'] == 'russian_cities':
        links, city = game.run_cities()
        GAME_STATUS['running'] = 'russian_cities'
        GAME_STATUS['russian_cities'] = city
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
        GAME_STATUS['running'] = 'countries'
        GAME_STATUS['countries'] = country
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


# Handler for game answers
@dp.message(lambda message: (GAME_STATUS['running'] == 'countries'))
async def process_countries_game_answer(message: Message):
    correct_answer = GAME_STATUS['countries']
    user_answer = message.text

    levenshtein_threshold = 3
    equivalent_names_lower = {name.lower(): equivalent_name if isinstance(equivalent_name, str) else equivalent_name[0].lower() for
                              equivalent_name, names in synonyms.equivalent_names.items() for name in
                              ([equivalent_name] if isinstance(equivalent_name, str) else equivalent_name)}

    user_answer_lower = user_answer.lower()
    correct = f'Правильно! Это {correct_answer}\nДля нового раунда игры напиши /next. Если хочешь закончить напиши' \
              f'/stop'
    incorrect = f'Неправильно. Это {correct_answer}\nДля нового раунда игры напиши /next. Если хочешь закончить' \
                f'напиши /stop'

    if user_answer_lower in equivalent_names_lower:
        if equivalent_names_lower[user_answer_lower] == correct_answer.lower():
            await message.answer(
                text=correct,
            )
        else:
            await message.answer(
                text=incorrect,
            )
        return

    # Сравниваем введенный ответ с правильным по расстоянию Левенштейна
    if distance(correct_answer.lower(), user_answer_lower) <= levenshtein_threshold:
        await message.answer(
            text=correct
        )
    else:
        await message.answer(
            text=incorrect,
        )

'''
# pip install python-Levenshtein

Эмпирическим путем было выбрано значение параметра threshold=3
(расстояние Левенштейна 0: точное совпадение между двумя строками, расстояние Левенштейна 1: одно изменение (вставка, удаление или замена одного символа) между строками и так далее)

def check_answer(user_answer, correct_answer, threshold=3):
    return distance(correct_answer.lower(), user_answer.lower()) <= threshold

correct_answer = "Москва"
user_answer = "мосакава"
result = check_answer(user_answer, correct_answer)

if result:
    print(f"Ответ считается правильным: {user_answer}")
else:
    print(f"Ответ считается неправильным: {user_answer}")
'''
