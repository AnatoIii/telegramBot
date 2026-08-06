"""
Simple Telegram bot with /test1, /test2, /test3 commands.
Each command replies with "It is N%" where N is a random number (0-100).
 
SETUP:
1. Install dependency:
     pip install python-telegram-bot --upgrade
 
2. Get a bot token from @BotFather on Telegram:
     - Open a chat with @BotFather
     - Send /newbot and follow the prompts
     - Copy the token it gives you
 
3. Set the token as an environment variable (recommended) or paste it below:
     export TELEGRAM_BOT_TOKEN="123456789:ABCdefGhIJKlmNoPQRstuVwxyZ"
 
4. Run the bot:
     python telegram_bot.py
 
5. In Telegram, open a chat with your bot and send:
     /test1
     /test2
     /test3
"""
 
import logging
import os
import random
 
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
 
# --- Configuration ---------------------------------------------------------
 
# Prefer an environment variable so you never hardcode secrets in the file.
# If you want to hardcode it for quick testing, replace the default below.
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8535182527:AAFPzqIDQX-FqzazGPQ0rOeYSnn9XbkXsHY")
 
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
 
 
# --- Command handlers --------------------------------------------------------
 
async def random_percent_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shared handler: replies with a random percentage."""
    n = random.randint(0, 100)
    await update.message.reply_text(f"It is {n}%")
 
 
async def howcossacksami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await random_percent_reply(update, context)
 
 
async def test2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await random_percent_reply(update, context)
 
 
async def test3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await random_percent_reply(update, context)
 
 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! Try one of these commands:\n/test1\n/test2\n/test3"
    )
 
 
# --- Entry point -------------------------------------------------------------
 
def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == "PUT_YOUR_TOKEN_HERE":
        raise RuntimeError(
            "No bot token found. Set the TELEGRAM_BOT_TOKEN environment variable "
            "or edit BOT_TOKEN in this file."
        )
 
    application = Application.builder().token(BOT_TOKEN).build()
 
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("howcossacksami", howcossacksami))
 
    logger.info("Bot is starting (polling mode)...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
 
 
if __name__ == "__main__":
    main()
