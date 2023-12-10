from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart
import keyboards
import Game_formation.start_game as game

# TODO: Добавить статус второго режима
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
        text='Привет. Это бот для игры в Geoguesser. Давай играть!',
        reply_markup=keyboards.start_keyboard
    )


# TODO: Дописать правила
# Handler for play button
# It will send message with mode_choice_keyboard
@dp.callback_query(F.data == 'play_button_pressed')
async def process_play_button_press(callback: CallbackQuery):
    await callback.message.answer(
        text='Выбери режим игры\n'
             'Города России:...\n'
             'Страны:...',
        reply_markup=keyboards.mode_choice_keyboard
    )


# Handler for support button
# It will send message with support_keyboard
@dp.callback_query(F.data == 'support_button_pressed')
async def process_support_button_press(callback: CallbackQuery):
    await callback.message.answer(
        text='Напишите ваше сообщение в поддержку',
        reply_markup=keyboards.support_keyboard
    )


# Handler for info button
# It will send message with info_keyboard
@dp.callback_query(F.data == 'info_button_pressed')
async def process_info_button_press(callback: CallbackQuery):
    await callback.message.answer(
        text='Полные правила',
        reply_markup=keyboards.info_keyboard
    )


# Handler for menu button
# It will send message with start_keyboard
@dp.callback_query(F.data == 'menu_button_pressed')
async def process_menu_button_press(callback: CallbackQuery):
    await callback.message.answer(
        text='Привет. Это бот для игры в Geoguesser. Давай играть!',
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
        InputMediaPhoto(media=links[0], caption='Попробуй угадать, какой это город. Напиши его название\n'
                                                'Если хочешь закончить игру напиши /stop'),
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
        InputMediaPhoto(media=links[0], caption='Попробуй угадать страну. Напиши её название\n'
                                                'Если хочешь закончить игру напиши /stop'),
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
        text='Выбери режим игры\n'
             'Города России:...\n'
             'Second_mode:...',
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
            InputMediaPhoto(media=links[0], caption='Попробуй угадать, какой это город. Напиши его название\n'
                                                    'Если хочешь закончить игру напиши /stop'),
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
            InputMediaPhoto(media=links[0], caption='Попробуй угадать страну. Напиши её название\n'
                                                    'Если хочешь закончить игру напиши /stop'),
            InputMediaPhoto(media=links[1]),
            InputMediaPhoto(media=links[2]),
            InputMediaPhoto(media=links[3]),
            InputMediaPhoto(media=links[4])
        ]
        await message.answer_media_group(
            media=message_data
        )


# Handler for game answers
@dp.message(lambda message: (GAME_STATUS['running'] != 'no'))
async def process_game_answer(message: Message):
    # TODO: Обработка вариативности
    if message.text == GAME_STATUS[GAME_STATUS['running']]:
        await message.answer(
            text='Правильно! Это ' + GAME_STATUS[GAME_STATUS['running']] + '\n'
                 'Для нового раунда игры напиши /next. Если хочешь закончить напиши /stop'
        )
    else:
        await message.answer(
            text='Не правильно. Это ' + GAME_STATUS[GAME_STATUS['running']] + '\n' 
                 'Для нового раунда игры напиши /next. Если хочешь закончить напиши /stop',
        )
