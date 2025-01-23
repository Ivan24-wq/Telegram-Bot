import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import Command
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
id_channel = os.getenv("id_channel")

bot = Bot(token=API_TOKEN)

dp = Dispatcher()

#обработчик перепостинга
@dp.message(F.text)  
async def commands(message: Message):
    if id_channel:
        await bot.send_message(chat_id=id_channel, text=message.text)


#Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())