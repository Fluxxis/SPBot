import asyncio
import json
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# === ДАННЫЕ ХРАНЯТСЯ ПРЯМО В ЭТОМ ФАЙЛЕ ===
BOT_TOKEN = "8068075516:AAFGT1zbPQYa2zbne7e576vjgdeF4Pv4oLY"
ADMIN_CHAT_ID = 7225974704  # <-- твой Telegram ID числом
WEBAPP_URL = "https://sp-web-dun.vercel.app/site/index.html"  # <-- https ссылка на WebApp
# =========================================

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

def with_chat_id(url: str, chat_id: int) -> str:
    return url + ("&" if "?" in url else "?") + f"chatId={chat_id}"

@dp.message(Command("start"))
async def start(message: types.Message):
    wa_url = with_chat_id(WEBAPP_URL, message.chat.id)

    kb = InlineKeyboardBuilder()
    kb.button(text="Открыть WebApp", web_app=WebAppInfo(url=wa_url))

    await message.answer_photo(
        photo=types.FSInputFile("assets/1.png"),
        caption="Нажми кнопку ниже, чтобы открыть WebApp",
        reply_markup=kb.as_markup(),
    )

    u = message.from_user
    await bot.send_message(
        ADMIN_CHAT_ID,
        f"/start from @{(u.username if u else None)} (id={(u.id if u else None)})"
    )

@dp.message(F.web_app_data)
async def on_webapp_data(message: types.Message):
    raw = message.web_app_data.data if message.web_app_data else ""
    u = message.from_user
    header = f"from @{(u.username if u else None)} (id={(u.id if u else None)})"

    try:
        data = json.loads(raw)
    except Exception:
        await bot.send_message(ADMIN_CHAT_ID, f"⚠️ WebApp data (unparsed) {header}\n{raw}")
        return

    t = data.get("type")
    if t == "opened":
        await bot.send_message(ADMIN_CHAT_ID, f"✅ WebApp opened {header}")
        return

    if t == "submit":
        fields = data.get("fields") or {}
        lines = [f"✅ Form submit {header}"]
        if isinstance(fields, dict):
            # Переименуем поля для читаемости (в WebApp они называются color/animal)
            pretty = {
                "color": "login_or_email",
                "animal": "message_to_admin",
            }
            for k, v in fields.items():
                lines.append(f"{pretty.get(k, k)}: {v}")
        else:
            lines.append(f"data: {fields}")
        await bot.send_message(ADMIN_CHAT_ID, "\n".join(lines))
        return

    await bot.send_message(ADMIN_CHAT_ID, f"ℹ️ WebApp event {header}\n{json.dumps(data, ensure_ascii=False)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
