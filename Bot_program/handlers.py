from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
import keyboards

dp = Dispatcher()

# Handler for "/start" command
# It will send message with start_keyboard
@dp.message(filters.CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Привет. Это бот для игры в Geoguesser. Давай играть!',
        reply_markup=keyboards.start_keyboard
    )

# TODO: Поменять название режимов
# Handler for play button
# It will send message with mode_choice_keyboard
@dp.callback_query(F.data == 'play_button_pressed')
async def process_play_button_press(callback: CallbackQuery):
    await callback.message.answer(
        text='Выбери режим игры\n'
             'First_mode:...\n'
             'Second_mode:...',
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
