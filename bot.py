import os
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters

# Bot Configuration
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# Initialize Pyrogram Client
bot = Client(
    "TeraBoxBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def get_direct_terabox_link(terabox_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    response = requests.get(terabox_url, headers=headers)
    if response.status_code != 200:
        return "❌ Error: Unable to fetch TeraBox page."
    
    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup.find_all("script"):
        if "videoPlayUrl" in script.text:
            start_index = script.text.find("videoPlayUrl") + len("videoPlayUrl") + 3
            end_index = script.text.find('"', start_index)
            direct_link = script.text[start_index:end_index]
            return direct_link
    
    return "❌ Error: No direct link found."

@bot.on_message(filters.command(["start", "help"]))
def start(client, message):
    message.reply_text("👋 Welcome! Send me a TeraBox link, and I'll generate a direct playable video link for you.")

@bot.on_message(filters.text & filters.private)
def fetch_terabox_link(client, message):
    url = message.text.strip()
    if "terabox.com/s/" not in url:
        message.reply_text("❌ Invalid TeraBox link. Please send a valid link.")
        return
    
    message.reply_text("🔄 Fetching direct link... Please wait!")
    direct_link = get_direct_terabox_link(url)
    message.reply_text(f"🎥 Here is your direct playable link:
{direct_link}")

# Run the bot
bot.run()
