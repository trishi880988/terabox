import os
import logging
import pymongo
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB setup
client = pymongo.MongoClient(MONGO_URI)
db = client['terabox_bot']
users_col = db['users']

# Function to generate playable link
def generate_link(terabox_link):
    encoded_link = terabox_link.replace("https://1024terabox.com/s/", "")
    return f"https://player.terabox.tech/?url=https%3A%2F%2F1024terabox.com%2Fs%2F{encoded_link}"

# Start command
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    users_col.update_one({"user_id": user.id}, {"$set": {"username": user.username}}, upsert=True)
    await update.message.reply_text("👋 Welcome! Send a TeraBox link to get a direct playable link.")

# Handle messages
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    if "terabox.com/s/" in text:
        playable_link = generate_link(text)
        response = (f"🎉 *Here's your link:*\n\n"
                    f"🔗 *Original Link:* {text}\n"
                    f"▶️ *Player Link:* {playable_link}\n\n"
                    f"**Bot developed by Gaurav Rajput**\n"
                    f"Join - @skillwithgaurav")
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Please send a valid TeraBox link.")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()

if __name__ == '__main__':
    main()
