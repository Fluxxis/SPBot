import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()

BOT_TOKEN = os.getenv("8068075516:AAGQywoJP1uUyC4XxV4jxHJ6Xhk39ScKFZ4")
ADMIN_CHAT_ID = os.getenv("7225974704")
WEBAPP_URL = os.getenv("https://sp-web-dun.vercel.app/site/index.html")

if not BOT_TOKEN:
    raise SystemExit("Missing BOT_TOKEN")
if not ADMIN_CHAT_ID:
    raise SystemExit("Missing ADMIN_CHAT_ID")
if not WEBAPP_URL:
    raise SystemExit("Missing WEBAPP_URL")

ADMIN_CHAT_ID_INT = int(ADMIN_CHAT_ID)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    # В приватном чате chat.id == user id. Мы прокидываем chatId в URL, чтобы WebApp/backend знали, откуда пользователь пришёл.
    chat_id = message.chat.id

    kb = InlineKeyboardBuilder()
    kb.button(
        text="Открыть Starpets",
        web_app=WebAppInfo(url=f"{WEBAPP_URL}?chatId={chat_id}")
    )

    await message.answer_photo(
        photo=types.FSInputFile("assets/1.png"),
        caption="Нажми кнопку ниже, чтобы открыть обновлённую версию Starpets",
        reply_markup=kb.as_markup(),
    )

    # Уведомление админу о старте (опционально, но удобно)
    await bot.send_message(ADMIN_CHAT_ID_INT, f"/start from @{message.from_user.username} (id={message.from_user.id})")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
