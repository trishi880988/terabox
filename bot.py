import os
import requests
from pyrogram import Client, filters

# ✅ Bot Configuration
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# ✅ Pyrogram Client
bot = Client("TeraBoxBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ TeraBox Direct Link Function
def get_direct_link(terabox_url):
    response = requests.get(f"https://api.example.com/getlink?url={terabox_url}")
    if response.status_code == 200:
        return response.json().get("direct_link")
    return None

# ✅ Command to Handle TeraBox Links
@bot.on_message(filters.command("start") & filters.private)
def start(client, message):
    message.reply_text("👋 Welcome! Send me a TeraBox link, and I'll get a direct playable link for you.")

@bot.on_message(filters.text & filters.private)
def fetch_link(client, message):
    url = message.text.strip()
    if "terabox.com" in url:
        direct_link = get_direct_link(url)
        if direct_link:
            message.reply_text(f"🎥 Here is your direct playable link:\n{direct_link}")
        else:
            message.reply_text("⚠️ Failed to generate a direct link. Please try again later.")
    else:
        message.reply_text("❌ Please send a valid TeraBox link.")

# ✅ Start Bot
print("🤖 Bot is running...")
bot.run()
