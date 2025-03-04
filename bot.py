import os
import logging
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Create Pyrogram Client
bot = Client(
    "TeraBoxBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# Function to convert TeraBox link to direct link
def get_direct_link(terabox_url):
    try:
        response = requests.get(terabox_url, allow_redirects=True)
        if response.status_code == 200:
            return response.url  # This returns the direct video link
        else:
            return None
    except Exception as e:
        logger.error(f"Error getting direct link: {e}")
        return None

# Command Handler for /start
@bot.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply_text("👋 Welcome! Send me a TeraBox link and I'll generate a direct video link for you.")

# Handler for receiving TeraBox links
@bot.on_message(filters.text & filters.private)
def handle_terabox_link(client, message: Message):
    terabox_url = message.text.strip()
    
    if "terabox.com" in terabox_url:
        message.reply_text("🔄 Processing your link, please wait...")
        direct_link = get_direct_link(terabox_url)
        
        if direct_link:
            message.reply_text(f"✅ Here is your direct link: {direct_link}\nClick to play the video instantly!")
        else:
            message.reply_text("❌ Failed to fetch direct link. Please try again later.")
    else:
        message.reply_text("⚠️ Please send a valid TeraBox link.")

# Run the bot
if __name__ == "__main__":
    bot.run()
