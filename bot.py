# bot.py

from pyrogram import Client, filters
from commands.new_member_handler import new_member_join
from commands.start_command import start_command
from commands.log_message import log_message

# Replace these placeholders with your actual values
API_ID = "29812636"
API_HASH = "581c6dd6f0af0f8c8326c9b28920ae54"
BOT_TOKEN = "6677982267:AAEcndDulVI6f9y4k_xC4UAVnY4vEPGzVU8"
LOG_CHANNEL_ID = -1002016756529  # Replace with your log channel ID
START_PICTURE_URL = "https://telegra.ph/file/240720bec6145bb269f17.jpg"  # Replace with your start picture URL

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
