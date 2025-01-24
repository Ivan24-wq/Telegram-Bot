import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import Command
import logging
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
id_channel = os.getenv("id_channel") 
target_id_channel = os.getenv("target_id_channel") 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command(commands=["start"]))
async def command_start(message: Message):
    await message.answer("Бот запущен и готов пересылать сообщения.")

# Пересылка сообщений из канала-источника в целевой канал
@dp.message(F.chat.type == "channel", F.chat.id == id_channel)
async def repost_message(message: Message):
    try:
        # Логирование
        logger.info(f"Новое сообщение из канала-источника: {message.message_id}")
        
        # Обработка текста
        if message.text:
            await bot.send_message(chat_id=target_id_channel, text=message.text)
        
        # Обработка фото
        elif message.photo:
            await bot.send_photo(chat_id=target_id_channel, photo=message.photo[-1].file_id, caption=message.caption)
        
        # Обработка видео
        elif message.video:
            await bot.send_video(chat_id=target_id_channel, video=message.video.file_id, caption=message.caption)
        
        # Обработка документов
        elif message.document:
            await bot.send_document(chat_id=target_id_channel, document=message.document.file_id, caption=message.caption)
        
        # Обработка аудио
        elif message.audio:
            await bot.send_audio(chat_id=target_id_channel, audio=message.audio.file_id, caption=message.caption)
        
        # Если тип сообщения не поддерживается
        else:
            logger.warning(f"Неизвестный формат сообщения: {message.message_id}")
    
    except Exception as e:
        logger.error(f"Ошибка при пересылке сообщения: {e}")

# Проверка прав бота при добавлении в канал
@dp.chat_member(ChatMemberUpdated)
async def check_bot_rights(event: ChatMemberUpdated):
    if event.new_chat_member.user.id == (await bot.get_me()).id:
        if not event.new_chat_member.is_chat_admin():
            logger.error(f"Бот добавлен в канал {event.chat.id}, но не является администратором.")
        else:
            logger.info(f"Бот добавлен в канал {event.chat.id} и имеет права администратора.")

# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
