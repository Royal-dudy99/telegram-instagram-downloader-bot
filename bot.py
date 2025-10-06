import os
import yt_dlp
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from io import BytesIO

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")


class InstagramDownloader:
    def __init__(self):
        pass
    
    def download_media(self, url):
        try:
            ydl_opts = {
                'noplaylist': True,
                'quiet': True,
                'socket_timeout': 10,  # Set timeout for extraction
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url')
                if video_url:
                    # Download with timeout and streaming
                    response = requests.get(video_url, timeout=20, stream=True)
                    if response.status_code == 200:
                        # Check file size first
                        content_length = response.headers.get('content-length')
                        if content_length:
                            file_size = int(content_length)
                            if file_size > 50 * 1024 * 1024:  # 50MB limit
                                return None, "too_large"
                        
                        # Download content
                        content = b""
                        for chunk in response.iter_content(chunk_size=8192):
                            content += chunk
                            if len(content) > 50 * 1024 * 1024:  # 50MB limit
                                return None, "too_large"
                        
                        return BytesIO(content), 'video'
        except Exception as e:
            print(f"Error: {e}")
            return None, None
        return None, None

downloader = InstagramDownloader()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Instagram Video Downloader Bot\n\n"
        "Send me any Instagram post or reel link and I'll send you the video/image file!\n\n"
        "Example: https://www.instagram.com/p/xxxxx/"
    )

async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    
    if 'instagram.com' not in message_text:
        await update.message.reply_text("❌ Please send a valid Instagram link!")
        return
    
    loading_msg = await update.message.reply_text("⏳ Downloading... Please wait!")
    
    try:
        media_data, media_type = downloader.download_media(message_text)
        
        if media_data and media_type == 'video':
            # Send video with increased timeout
            await update.message.reply_video(
                video=media_data,
                caption="✅ Downloaded successfully!",
                filename='instagram_video.mp4',
                read_timeout=60,  # Increased timeout
                write_timeout=60,  # Increased timeout
                connect_timeout=60  # Increased timeout
            )
            await loading_msg.delete()
        elif media_type == "too_large":
            await loading_msg.edit_text("❌ Video is too large (>50MB). Telegram has a 50MB limit for bot uploads.")
        else:
            await loading_msg.edit_text("❌ Failed to download. Please try a different Instagram link or try again later.")
            
    except Exception as e:
        print(f"Exception occurred: {e}")
        await loading_msg.edit_text("❌ Download failed. Please try again with a shorter video.")

def main():
    # Build application with increased timeouts
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .read_timeout(60)    # Increased from default 5s
        .write_timeout(60)   # Increased from default 5s
        .connect_timeout(60) # Increased from default 5s
        .build()
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))
    
    print("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    main()
