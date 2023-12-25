import asyncio
from aiogram import Bot
import handlers


BOT_TOKEN = ''

bot = Bot(token=BOT_TOKEN)


async def main() -> None:
    await handlers.dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
