from pyrogram import Client, filters
from pyrogram.types import Message

# Importing configuration from config.py
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_USER_IDS

# Initialize the Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

## Custom filter to check if the user is an admin
def is_admin(_, __, message: Message):
    return message.from_user.id in ADMIN_USER_IDS
 

# Handler for the /start command
@app.on_message(filters.command("start") & is_admin)
async def start_command(client, message: Message):
    # Prompt the admin to set the image and caption
    await message.reply_text("Please set the image and caption.")

    # Set the next handler to handle image and caption setting
    await app.set_next_step(chat_id=message.chat.id, action=set_image_and_caption)

# Handler to handle image and caption setting
async def set_image_and_caption(client, message: Message):
    # Check if the message contains an image
    if message.photo:
        # Get the photo
        photo = message.photo[-1]
        # Download the photo
        photo_path = await photo.download(file_name="image.jpg")

        # Set the image and caption
        app.image_path = photo_path
        app.caption = message.text

        # Ask the admin to send the file
        await message.reply_text("Please send the file.")
    else:
        # If the message does not contain an image, ask the admin to resend
        await message.reply_text("Please send the image as a photo.")

# Handler for file sent by the admin
@app.on_message(is_admin)
async def handle_file(client, message: Message):
    # Check if the bot has set the image and caption
    if hasattr(app, 'image_path') and hasattr(app, 'caption'):
        # Check if the message contains a file
        if message.document:
            # Download the file
            file_path = await message.download(file_name="file")

            # Send the file with the set caption
            await message.reply_photo(photo=app.image_path, caption=app.caption)

            # Delete the message after sending the file
            await message.delete()
        else:
            # If the message does not contain a file, ask the admin to resend
            await message.reply_text("Please send the file.")
    else:
        # If the bot has not set the image and caption, ignore the file
        pass

# Start the Pyrogram Client
app.run()
