# bot.py

from pyrogram import Client, filters
from commands.new_member_handler import new_member_join
from commands.start_command import start_command
from commands.log_message import log_message

# Replace these placeholders with your actual values
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
LOG_CHANNEL_ID = -100123456789  # Replace with your log channel ID
START_PICTURE_URL = "URL_TO_YOUR_START_PICTURE"  # Replace with your start picture URL

# Initialize the Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register the handler for new member join events
app.on_message(filters.new_chat_members)(new_member_join)

# Register the handler for the start command
app.on_message(filters.command("start"))(start_command)

# Register the message handler to log messages
app.add_handler(log_message)

# Start the Pyrogram Client
app.run()
