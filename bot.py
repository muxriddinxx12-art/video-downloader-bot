import asyncio
import logging
import os
import re

import yt_dlp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from config import BOT_TOKEN, DOWNLOAD_DIR, MAX_FILE_SIZE_MB
from downloader import download_video

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

URL_REGEX = re.compile(r"https?://\S+")


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Salom! 👋\n\n"
        "Menga video havolasini yuboring (YouTube, Instagram, TikTok, "
        "Twitter/X va h.k.), men uni yuklab, shu yerga yuboraman.\n\n"
        "Masalan:\n"
        "https://www.youtube.com/watch?v=xxxxx"
    )


@dp.message(F.text.regexp(URL_REGEX))
async def download_handler(message: Message):
    match = URL_REGEX.search(message.text)
    if not match:
        return
    url = match.group(0)

    status_msg = await message.answer("⏳ Video yuklanmoqda, biroz kuting...")

    filepath = None
    try:
        loop = asyncio.get_event_loop()
        filepath = await loop.run_in_executor(None, download_video, url)

        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            await status_msg.edit_text(
                f"❌ Video juda katta ({size_mb:.1f}MB). "
                f"Telegram bot orqali {MAX_FILE_SIZE_MB}MB dan katta fayl yuborib bo'lmaydi."
            )
            return

        await status_msg.edit_text("📤 Yuklandi, yuborilmoqda...")
        video_file = FSInputFile(filepath)
        await message.answer_video(video_file, caption="✅ Mana sizning videongiz!")
        await status_msg.delete()

    except yt_dlp.utils.DownloadError as e:
        error_text = str(e)[:500]
        await status_msg.edit_text(f"❌ Yuklab bo'lmadi:\n\n{error_text}")
        logging.error(f"Download error: {e}")
    except Exception as e:
        error_text = str(e)[:500]
        await status_msg.edit_text(f"❌ Xatolik:\n\n{error_text}")
        logging.error(f"Unexpected error: {e}")
    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)


@dp.message()
async def fallback_handler(message: Message):
    await message.answer("Iltimos, menga video havolasini yuboring 🔗")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
