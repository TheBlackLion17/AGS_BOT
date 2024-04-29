from pyrogram import Client, filters
from pyrogram.types import Message

# Importing configuration from config.py
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store the state of the conversation for each user
conversation_state = {}

# Handler for the /start command
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    # Set the state of the conversation to "awaiting_image_and_caption"
    conversation_state[message.chat.id] = "awaiting_image_and_caption"
    
    # Prompt the user to set the image and caption
    await message.reply_text("Please set the image and caption.")

# Handler for messages
@app.on_message()
async def handle_message(client, message: Message):
    # Check if the user is in the "awaiting_image_and_caption" state
    if message.chat.id in conversation_state and conversation_state[message.chat.id] == "awaiting_image_and_caption":
        # Check if the message contains an image
        if message.photo:
            # Get the largest photo size
            photo = message.photo
            file_id = photo.file_id
            # Get the photo file object using the file ID
            photo_file = await client.get_file(file_id)
            # Download the photo
            photo_path = await photo_file.download(file_name="image.jpg")

            # Set the state of the conversation to "awaiting_file"
            conversation_state[message.chat.id] = "awaiting_file"

            # Set the image path and caption in the conversation state
            conversation_state[message.chat.id + "_image_path"] = photo_path
            conversation_state[message.chat.id + "_caption"] = message.text

            # Prompt the user to send the file
            await message.reply_text("Please send the file.")
        else:
            # If the message does not contain an image, ask the user to resend
            await message.reply_text("Please send the image as a photo.")
    # Check if the user is in the "awaiting_file" state
    elif message.chat.id in conversation_state and conversation_state[message.chat.id] == "awaiting_file":
        # Check if the message contains a file
        if message.document:
            # Download the file
            file_path = await message.download(file_name="file")

            # Send the file with the set caption
            await message.reply_photo(
                photo=conversation_state[message.chat.id + "_image_path"],
                caption=conversation_state[message.chat.id + "_caption"]
            )

            # Delete the message after sending the file
            await message.delete()

            # Clear the conversation state
            del conversation_state[message.chat.id]
            del conversation_state[message.chat.id + "_image_path"]
            del conversation_state[message.chat.id + "_caption"]
        else:
            # If the message does not contain a file, ask the user to resend
            await message.reply_text("Please send the file.")

app.run()
