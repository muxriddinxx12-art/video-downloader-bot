except yt_dlp.utils.DownloadError as e:
        error_text = str(e)[:500]  # xabar uzun bo'lmasligi uchun cheklaymiz
        await status_msg.edit_text(f"❌ Yuklab bo'lmadi:\n\n{error_text}")
        logging.error(f"Download error: {e}")
    except Exception as e:
        error_text = str(e)[:500]
        await status_msg.edit_text(f"❌ Xatolik:\n\n{error_text}")
        logging.error(f"Unexpected error: {e}")
    
