from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Pyrogram client
app = Client("autofilter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# List to store filter keywords
filters_list = []


# Command to start the bot
@app.on_message(filters.command("start"))
def start(_, update):
    update.reply_text("Hello! I'm an auto-filter bot. Send me a message and I'll filter it for you.")


# Command to add a filter with custom button
@app.on_message(filters.command("addfilter") & filters.private)
def add_filter_command(_, update):
    # Get the text after the command
    text = update.text.split(maxsplit=1)
    if len(text) == 2:
        keyword_and_button = text[1].strip()
        if ":" in keyword_and_button and keyword_and_button.startswith("[") and keyword_and_button.endswith(")"):
            keyword, button_data = keyword_and_button[1:-1].split("](")
            button_text, button_url = button_data.split("://")
            if keyword not in filters_list:
                filters_list.append(keyword)
                update.reply_text(f"Filter '{keyword}' with custom button added successfully!")
            else:
                update.reply_text(f"Filter '{keyword}' already exists!")
        else:
            update.reply_text("Please provide a valid filter with custom button in the format: [name](buttonurl://example.com:same)")
    else:
        update.reply_text("Please provide a filter with custom button in the format: [name](buttonurl://example.com:same)")


# Auto-filter function
@app.on_message(~filters.private)
def auto_filter(_, update):
    for keyword in filters_list:
        if keyword in update.text.lower():
            # If the keyword is found, reply with the filtered message with custom button
            button_text, button_url = "Click Here", "https://example.com"  # Default button data
            if ":same" not in keyword:
                button_text, button_url = keyword.split(":")
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=button_url)]])
            update.reply_text(f"Filtered message: {update.text}", reply_markup=reply_markup)
            return


# Run the bot
app.run()
