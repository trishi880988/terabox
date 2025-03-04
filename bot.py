import os
import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ⬇️ Bot Token & Config
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8443))

# ⬇️ TeraBox Direct Video Link Generator
def generate_link(original_link):
    try:
        encoded_url = requests.utils.quote(original_link, safe="")
        direct_link = f"https://player.terabox.tech/?url={encoded_url}"
        return direct_link
    except Exception as e:
        return None

# ⬇️ Start Command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "**Welcome to TeraBox Video Link Bot! 🎬**\n\n"
        "Just send me a **TeraBox link**, and I'll generate a **direct playable link** for you. 🚀",
        parse_mode=ParseMode.MARKDOWN
    )

# ⬇️ Handle TeraBox Links
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if "terabox.com" in text:
        direct_link = generate_link(text)

        if direct_link:
            response = (
                f"🎉 **Here's your link:**\n\n"
                f"🔗 **Original Link:** {text}\n\n"
                f"▶️ **Player Link:** {direct_link}\n\n"
                f"**Bot developed by Gaurav Rajput**\n"
                f"👉 Join - @skillwithgaurav"
            )
        else:
            response = "❌ **Error:** Unable to generate the direct link."

        update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("❌ **Error:** Please send a valid **TeraBox link**.")

# ⬇️ Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Deploy for Heroku
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.setWebhook(f"https://{os.getenv('HEROKU_APP_NAME')}.herokuapp.com/{TOKEN}")

    updater.idle()

if __name__ == "__main__":
    main()
