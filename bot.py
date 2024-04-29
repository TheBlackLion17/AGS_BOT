# bot.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_USER_ID

# Initialize the Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Custom filter to match messages with the specified button callback data
@filters.create(lambda _, __, update: update.message and update.message.reply_to_message and update.message.reply_to_message.from_user.is_self)
def button_callback_filter(_, __, update):
    return update.data == "send_file_button"

# Handler for the command to trigger sending the message with the button
@app.on_message(filters.command("sendfile"))
def send_file_command(client, message):
    # Check if the user is the admin
    if message.from_user.id == ADMIN_USER_ID:
        # Reply with instructions
        message.reply_text("Please send me the image and text for the caption. The image should be sent as a photo.")

        # Set the next handler
        app.register_next_step_handler(message, handle_image_and_text)
    else:
        message.reply_text("You are not authorized to use this command.")

# Handler to handle image and text sent by the admin
def handle_image_and_text(client, message):
    # Check if the message is a photo
    if message.photo:
        # Get the largest available photo
        photo = message.photo[-1]
        # Download the photo
        photo_path = photo.download(file_name="image.jpg")

        # Get the text for the caption
        caption = message.text

        # Send the file
        message.reply_photo(photo_path, caption=caption)

        # Sleep for 60 seconds
        time.sleep(60)

        # Delete the message after 60 seconds
        message.delete()
    else:
        # If the message is not a photo, ask the admin to resend
        message.reply_text("Please send the image as a photo.")

# Start the Pyrogram Client
app.run()
