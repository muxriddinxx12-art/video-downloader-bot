import os
import uuid

import yt_dlp

from config import DOWNLOAD_DIR


def build_ydl_opts(file_id: str) -> dict:
    output_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")
    return {
        "outtmpl": output_template,
        "format": "best[filesize<50M]/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }


def download_video(url: str) -> str:
    file_id = str(uuid.uuid4())
    ydl_opts = build_ydl_opts(file_id)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)

    if not os.path.exists(filepath):
        base, _ = os.path.splitext(filepath)
        candidate = base + ".mp4"
        if os.path.exists(candidate):
            filepath = candidate

    return filepath
