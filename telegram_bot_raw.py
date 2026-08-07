"""
Telegram bot with a single /howgayami command — built WITHOUT any
Telegram-specific library. It talks to the Telegram Bot API directly over
plain HTTP using `requests` and does its own long-polling loop.

Note: Telegram only allows lowercase letters, digits, and underscores in
command names, so the command is registered as /howgayami (not /HowGayAmI).
It's matched case-insensitively below, so /HowGayAmI typed by a user still works.

SETUP:
1. Install the only dependency:
     pip install requests

2. Get a bot token from @BotFather on Telegram (send /newbot, follow prompts).

3. Set the token as an environment variable:
     export TELEGRAM_BOT_TOKEN="123456789:ABCdefGhIJKlmNoPQRstuVwxyZ"

4. Run:
     python telegram_bot_raw.py

5. In Telegram, message your bot with /howgayami.

HOW IT WORKS:
Telegram's Bot API is just plain HTTP/JSON. This script repeatedly calls
`getUpdates` (long polling) to fetch new messages, checks if the message
text is the known command, and calls `sendMessage` to reply. No SDK needed.
"""

import json
import os
import random
import time

import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

COMMAND = "/howgayami"
BUTTON_LABEL = "🎲 How Gay Am I?"

# A reply keyboard: replaces the user's normal keyboard with these buttons.
# Tapping a button just sends its label text as a regular message.
MAIN_KEYBOARD = {
    "keyboard": [[{"text": BUTTON_LABEL}]],
    "resize_keyboard": True,   # make buttons compact instead of full-size
    "is_persistent": True,     # keep the keyboard showing after use
}


def get_updates(offset=None, timeout=30):
    """Long-poll Telegram for new updates (messages)."""
    params = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    resp = requests.get(f"{API_URL}/getUpdates", params=params, timeout=timeout + 10)
    resp.raise_for_status()
    return resp.json()["result"]


def send_message(chat_id, text, reply_markup=None):
    """Send a text message to a chat, optionally with a keyboard attached."""
    data = {"chat_id": chat_id, "text": text}
    if reply_markup is not None:
        data["reply_markup"] = json.dumps(reply_markup)
    resp = requests.post(f"{API_URL}/sendMessage", data=data, timeout=10)
    resp.raise_for_status()
    return resp.json()


def handle_update(update):
    message = update.get("message")
    if not message or "text" not in message:
        return

    text = message["text"].strip()
    chat_id = message["chat"]["id"]

    # Handle "/howgayami" and also "/howgayami@YourBotName" (used in group chats),
    # case-insensitively.
    command = text.split("@")[0].split()[0].lower() if text.startswith("/") else None

    if command == COMMAND or text == BUTTON_LABEL:
        n = random.randint(0, 100)
        send_message(chat_id, f"{n}%", reply_markup=MAIN_KEYBOARD)
    elif command == "/start":
        send_message(chat_id, "Hi! Tap the button below.", reply_markup=MAIN_KEYBOARD)


def main():
    if not BOT_TOKEN or BOT_TOKEN == "PUT_YOUR_TOKEN_HERE":
        raise RuntimeError(
            "No bot token found. Set TELEGRAM_BOT_TOKEN or edit BOT_TOKEN in this file."
        )

    print("Bot is starting (manual long-polling, no telegram library)...")
    offset = None

    while True:
        try:
            updates = get_updates(offset=offset)
            for update in updates:
                handle_update(update)
                offset = update["update_id"] + 1
        except requests.exceptions.RequestException as e:
            print(f"Network error, retrying in 5s: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()