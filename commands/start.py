# commands/start_command.py

from pyrogram.types import Message

# Handler for the start command
def start_command(client, message: Message):
    if START_PICTURE_URL:
        client.send_photo(
            chat_id=message.chat.id,
            photo=START_PICTURE_URL,
            caption="Welcome to the group! Feel free to introduce yourself."
        )
    else:
        message.reply_text("Welcome to the group! Feel free to introduce yourself.")
