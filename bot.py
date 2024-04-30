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
            await message.reply_text("Please provide a name and button text for the filter.")
            return
        
        # Unpack the components
        _, filter_name_and_button_text = components
        try:
            filter_name, button_text = filter_name_and_button_text.split(maxsplit=1)
        except ValueError:
            await message.reply_text("Please provide both filter name and button text.")
            return

        # Add the filter to the filters dictionary
        filters_dict[filter_name] = {
            "button_text": button_text
        }

        await message.reply_text(f"Filter '{filter_name}' added successfully.")
        return

# Handler for inline queries
@app.on_inline_query()
async def handle_inline_query(client, inline_query):
    results = []

    # Check if the inline query is from an admin
    if inline_query.from_user.id in ADMIN_ID:
        for filter_name, filter_data in filters_dict.items():
            if filter_name.lower() in inline_query.query.lower():
                results.append(
                    InlineQueryResultArticle(
                        title=filter_name,
                        input_message_content=InputTextMessageContent(
                            message_text=filter_name,
                            parse_mode="HTML"
                        ),
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton(filter_data["button_text"], switch_inline_query_current_chat=filter_name)]
                        ])
                    )
                )

    await inline_query.answer(results)

# Start the Pyrogram Client
app.run()
