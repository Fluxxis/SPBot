import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ⚠️ НЕБЕЗОПАСНО: значения зашиты в код.
# Если этот файл попадет в чужие руки (GitHub/архив/логи) — токен утечет и бот угонят.
# Делай так только если ты понимаешь риск.

# ВСТАВЬ СВОИ ДАННЫЕ СЮДА
BOT_TOKEN = "8068075516:AAHE20HCJmiC1hD-SKmyx1-TxhJWNi4PWPs"
ADMIN_CHAT_ID_INT = 7225974704  # например: 7225974704
WEBAPP_URL = "https://sp-web-dun.vercel.app/site/index.html"

if BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
    raise SystemExit("BOT_TOKEN is not set in bot.py")

if not isinstance(ADMIN_CHAT_ID_INT, int) or ADMIN_CHAT_ID_INT == 0:
    raise SystemExit("ADMIN_CHAT_ID_INT is not set in bot.py")

if not WEBAPP_URL:
    raise SystemExit("WEBAPP_URL is not set in bot.py")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    # In a private chat, chat.id == user id.
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

    # Optional: notify admin
    username = message.from_user.username or "(no_username)"
    await bot.send_message(
        ADMIN_CHAT_ID_INT,
        f"/start from @{username} (id={message.from_user.id})"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
