import os
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

# Function to generate player link
def generate_player_link(terabox_link: str) -> str:
    encoded_link = terabox_link.replace("https://", "").replace("/", "%2F")
    return f"https://player.terabox.tech/?url=https%3A%2F%2F{encoded_link}"

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a TeraBox link, and I'll generate a direct player link for you!")

# Message handler to process TeraBox links
def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    match = re.search(r'https?://1024terabox\.com/s/\S+', text)
    
    if match:
        original_link = match.group()
        player_link = generate_player_link(original_link)
        
        keyboard = [[InlineKeyboardButton("▶️ Watch Now", url=player_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        response = (f"\n\n<b>🎉 Here's your link:</b>\n\n"
                    f"🔗 <b>Original Link:</b> <code>{original_link}</code>\n\n"
                    f"▶️ <b>Player Link:</b> <a href='{player_link}'>Click Here to Watch</a>\n\n"
                    f"<b>Bot developed by Gaurav Rajput</b>\n"
                    f"Join - @skillwithgaurav")
        
        update.message.reply_text(response, reply_markup=reply_markup, parse_mode="HTML")
    else:
        update.message.reply_text("❌ Invalid TeraBox link. Please send a valid one!")

# Main function to start bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
