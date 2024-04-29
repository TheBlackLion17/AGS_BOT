from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Importing configuration from config.py
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID

# Initialize the Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store user-defined filters
filters_dict = {}

# Handler for messages
@app.on_message(filters.private & filters.user(ADMIN_ID))
async def handle_message(client, message: Message):
    # Check if the message is not None
    if message is None:
        return

    # Check if the message is a command to create a filter
    if message.text and message.text.startswith("/addfilter"):
        # Split the message into components
        components = message.text.split(maxsplit=1)

        # Check if the message contains enough components
        if len(components) < 2:
            await message.reply_text("Please provide a name for the filter.")
            return
        
        # Unpack the components
        _, filter_name = components

        # Add the pending filter to the dictionary
        await message.reply_text(f"Please send the document to attach to the filter '{filter_name}'.")
        return

    # Check if the message contains a document
    if message.document:
        # Store the document in the filter dictionary
        filters_dict[message.text] = message.document.file_id

        await message.reply_text(f"Filter '{message.text}' added successfully.")
        return

# Handler for messages from non-admin users
@app.on_message(filters.private & ~filters.user(ADMIN_IDS))
async def handle_message_non_admin(client, message: Message):
    # Check if the message is a filter name
    if message.text and message.text in filters_dict:
        # Send the document associated with the filter name
        await message.reply_document(filters_dict[message.text])

# Start the Pyrogram Client
app.run()
