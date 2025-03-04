import os
import logging
from pyrogram import Client, filters
import requests

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TeraBoxBot")

# Bot credentials (Set these in Heroku/Koyeb environment variables)
API_ID = int(os.getenv("API_ID", "your_api_id_here"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")

# Initialize bot
bot = Client("terabox_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# TeraBox API (Replace with actual working API if needed)
TERABOX_API = "https://terabox-dl-arman.vercel.app/api?data="

@bot.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("👋 Welcome! Send me a TeraBox link and I'll generate a playable video link for you.")

@bot.on_message(filters.text & filters.private)
def get_video_link(client, message):
    terabox_link = message.text.strip()
    if "terabox" not in terabox_link:
        message.reply_text("❌ Invalid link! Please send a valid TeraBox link.")
        return
    
    message.reply_text("🔄 Fetching playable link, please wait...")
    try:
        response = requests.get(TERABOX_API + terabox_link)
        data = response.json()
        if "error" in data:
            message.reply_text("❌ Failed to get video. Please check the link and try again.")
        else:
            playable_link = data.get("direct_link", "")
            message.reply_text(f"✅ Here is your video link:\n[Click to Play]({playable_link})", disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"Error fetching video link: {e}")
        message.reply_text("❌ Something went wrong. Please try again later.")

# Start bot
if __name__ == "__main__":
    bot.run()
