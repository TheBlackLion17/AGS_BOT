from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Importing configuration from config.py
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID

# Initialize the Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store user-defined filters
filters_dict = {}

# Dictionary to store documents sent by users
document_cache = {}

# Handler for messages
@app.on_message(filters.private & filters.user(ADMIN_ID))
async def handle_message(client, message: Message):
    # Check if the message is not None
    if message is None:
        return

    


    # Check if the message is a command to create a filter
    if message.text and message.text.startswith("/addfilter"):
        # Split the message into filter name, image caption, and button text
        _, filter_name, image_caption, button_text = message.text.split(maxsplit=3)

        # Add the filter to the filters dictionary
        filters_dict[filter_name] = {
            "image_caption": image_caption,
            "button_text": button_text
        }

        await message.reply_text(f"Filter '{filter_name}' added successfully.")
        return

    # Check if the message contains a document
    if message.document:
        # Store the document in the document cache
        document_cache[message.chat.id] = message.document

        await message.reply_text("Document received. You can now use the /addfilter command to create a filter.")
        return

# Handler for button click
@app.on_callback_query()
async def handle_button_click(client, callback_query):
    # Check if the button was clicked
    filter_name = callback_query.data
    if filter_name in filters_dict:
        filter_data = filters_dict[filter_name]
        
        # Get the document from the cache
        document = document_cache.get(callback_query.message.chat.id)
        if document:
            # Send the document
            await callback_query.message.reply_document(document.file_id, caption=filter_data["image_caption"])
        else:
            await callback_query.message.reply_text("No document found.")

# Start the Pyrogram Client
app.run()
