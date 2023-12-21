import asyncio
from aiogram import Bot
import handlers

# Вставьте токен бота | потом можно сделать это автоматически
# Только не делитесь токеном, он должен быть секретным!!!
BOT_TOKEN = '6768068988:AAHfjcqFw3ePunIwcN_VuklK4B46gl9VXUY'

bot = Bot(token=BOT_TOKEN)


async def main() -> None:
    await handlers.dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
