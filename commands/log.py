# commands/log_message.py

from pyrogram.types import Message

# Handler for logging messages to a designated channel
def log_message(client, message: Message):
    if message.from_user:
        log_message_text = f"User: {message.from_user.username} | Chat ID: {message.chat.id} | Message: {message.text}"
    else:
        log_message_text = f"Channel ID: {message.chat.id} | Message: {message.text}"
    
    client.send_message(LOG_CHANNEL_ID, log_message_text)
