from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to convert TeraBox link to a playable link
def get_playable_link(original_link: str) -> str:
    encoded_link = original_link.replace('https://', '').replace('/', '%2F')
    return f"https://player.terabox.tech/?url=https%3A%2F%2F{encoded_link}"

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a TeraBox link, and I'll generate a direct playable link for you!")

# Message handler for extracting TeraBox links
def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    match = re.search(r'https?://(?:www\.)?1024terabox\.com/s/\S+', text)
    if match:
        original_link = match.group()
        playable_link = get_playable_link(original_link)
        update.message.reply_text(f"🎉 Here's your link:\n\n🔗 Original Link: {original_link}\n\n▶️ Player Link: {playable_link}")
    else:
        update.message.reply_text("Please send a valid TeraBox link.")

# Main function to start the bot
def main():
    TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot's token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
