from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Importing configuration from config.py
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID

# Initialize the Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store user-defined filters
filters_dict = {}

# Handler for messages
@app.on_message()
async def handle_message(client, message: Message):
    # Check if the message is from an admin
    if message.from_user.id not in ADMIN_ID:
        await message.reply_text("You are not authorized to use this bot.")
        return
    
    # Check if the message is a command to create a filter
    if message.text.startswith("/addfilter"):
        # Split the message into filter name, image caption, and button text
        _, filter_name, image_caption, button_text = message.text.split(maxsplit=3)

        # Add the filter to the filters dictionary
        filters_dict[filter_name] = {
            "image_caption": image_caption,
            "button_text": button_text
        }

        await message.reply_text(f"Filter '{filter_name}' added successfully.")
        return

    # Check if the message matches any of the user-defined filters
    for filter_name, filter_data in filters_dict.items():
        if filter_name.lower() in message.text.lower():
            # Create an inline keyboard with a button
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(filter_data["button_text"], callback_data="button_clicked")]])
            
            # Reply with the image caption and the inline keyboard
            await message.reply_text(filter_data["image_caption"], reply_markup=keyboard)
            return

# Handler for button click
@app.on_callback_query()
async def handle_button_click(client, callback_query):
    # Check if the button was clicked
    if callback_query.data == "button_clicked":
        # Reply to the button click with a message
        await callback_query.answer("Button clicked!")

# Start the Pyrogram Client
app.run()
