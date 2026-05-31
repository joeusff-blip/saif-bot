import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7760043214:AAECtCgpC7bkhY1AhtRMnTGYbx9rohpDZz8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً! أنا بوت يوسف علشان اخلص من قروشة الولد الجبلي هذا\n\n"
        "📱 أرسل لي رابط من:\n"
        "• TikTok ✅\n"
        "• Instagram ✅\n\n"
        "وراح أحمله لك فوراً! 🚀"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if "tiktok.com" not in url and "instagram.com" not in url:
        await update.message.reply_text("❌ أرسل رابط TikTok أو Instagram فقط!")
        return
    
    msg = await update.message.reply_text("⏳ جاري التحميل...")
    
    try:
        os.makedirs("downloads", exist_ok=True)
        
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            title = info.get('title', 'فيديو')
        
        await msg.edit_text("✅ طيب قاعد احمل لاتقروشني افتكو ثمك! جاري الإرسال...")
        
        with open(file_path, 'rb') as video:
            await update.message.reply_video(
                video=video,
                caption=f"🎬 {title}\n\n⚡ بوت التحميل",
                supports_streaming=True
            )
        
        os.remove(file_path)
        await msg.delete()
        
    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ: {str(e)}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("✅ البوت شغال!")
    app.run_polling()

if __name__ == "__main__":
    main()