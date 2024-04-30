import io
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Pyrogram client
app = Client("sticker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store the user's current state (waiting for image)
user_state = {}


# Command to start the bot
@app.on_message(filters.command("start"))
def start(_, update):
    update.reply_text("Hello! I'm a sticker bot. Send me an image and I'll add text to it and turn it into a sticker for you!")


# Function to create sticker from image with text
def create_sticker(image_bytes, text):
    # Load the image
    img = Image.open(io.BytesIO(image_bytes))

    # Initialize drawing context
    draw = ImageDraw.Draw(img)

    # Load a font
    font = ImageFont.truetype("arial.ttf", 48)

    # Wrap text into lines
    lines = textwrap.wrap(text, width=10)

    # Calculate text size and position
    y_text = 10
    for line in lines:
        width, height = draw.textsize(line, font=font)
        draw.text(((img.width - width) / 2, y_text), line, font=font, fill="black")
        y_text += height + 10

    # Convert image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes


# Function to handle messages containing images
@app.on_message(filters.photo)
def image_to_sticker(_, update: Message):
    chat_id = update.chat.id

    if chat_id in user_state and user_state[chat_id] == "waiting_for_text":
        # Retrieve the image and text
        image_file_id = update.photo[-1].file_id
        text = update.caption

        # Download the image
        image_bytes = app.download_media(image_file_id)

        # Create sticker from image with text
        sticker_bytes = create_sticker(image_bytes, text)

        # Send the sticker
        update.reply_sticker(sticker_bytes)

        # Reset user state
        del user_state[chat_id]

    else:
        # Ask the user to send an image
        update.reply_text("Please send an image first.")


# Function to handle messages containing text
@app.on_message(filters.text)
def handle_text(_, update):
    chat_id = update.chat.id

    # Set user state to waiting for text
    user_state[chat_id] = "waiting_for_text"

    # Ask the user to send text
    update.reply_text("Please send the text you want to add to the image.")


# Run the bot
app.run()
