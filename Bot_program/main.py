import asyncio
from aiogram import Bot
import handlers


BOT_TOKEN = '6768068988:AAG7eCJfYkZwUyf1hxvpZ1vAH_6otou5klI'

bot = Bot(token=BOT_TOKEN)


async def main() -> None:
    await handlers.dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


