import logging
import json
from telegram import ForceReply, Update
import requests
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

users_data = {}

def save_users():
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users_data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = str(user.id)
    save_users()

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
    )
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "hi":
        await update.message.reply_text("hello")
    elif update.message.text == "bye":
        await update.message.reply_text("bye")
    else:
        await update.message.reply_text(update.message.text)
async def price_btc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    data = response.json()
    price = data["bitcoin"]["usd"]
    await update.message.reply_text(f"dollar: ${price}")
bot_data = {
    "log_level": logging.getLevelName(logger.level),
    "log_file": "console"
}
with open("bot_data.json", "w", encoding="utf-8") as f:
    json.dump(bot_data, f, ensure_ascii=False, indent=4)
def main() -> None:
    application = Application.builder().token("token section").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("price_btc", price_btc))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__ == "__main__":
    main()
