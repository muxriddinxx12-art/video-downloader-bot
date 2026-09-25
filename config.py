import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi! Uni muhit o'zgaruvchisi sifatida bering:\n"
        "  Linux/Mac: export BOT_TOKEN=your_token_here\n"
        "  Windows:   set BOT_TOKEN=your_token_here"
    )

DOWNLOAD_DIR = "downloads"
MAX_FILE_SIZE_MB = 50
