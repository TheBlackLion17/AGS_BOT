import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Pyrogram client
app = Client("autofilter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Regular expression pattern to match the specified format
pattern = r"\[(.*?)\]\(buttonurl://(.*?)\)"

# List to store filter keywords
filters_list = []


# Command to start the bot
@app.on_message(filters.command("start"))
def start(_, update):
    update.reply_text("Hello! I'm an auto-filter bot. Send me a message and I'll filter it for you.")


# Command to add a filter
@app.on_message(filters.command("addfilter") & filters.private)
def add_filter_command(_, update):
    # Get the text after the command
    text = update.text.split(maxsplit=1)
    if len(text) == 2:
        keyword = text[1].strip().lower()
        if keyword not in filters_list:
            filters_list.append(keyword)
            update.reply_text(f"Filter '{keyword}' added successfully!")
        else:
            update.reply_text(f"Filter '{keyword}' already exists!")
    else:
        update.reply_text("Please provide a keyword after the command.")


# Auto-filter function
@app.on_message(~filters.private)
def auto_filter(_, update):
    for keyword in filters_list:
        if keyword in update.text.lower():
            # If the keyword is found, extract the button URL and name
            match = re.search(pattern, update.text)
            if match:
                name = match.group(1)
                url = match.group(2)

                # Create the custom button
                button = InlineKeyboardButton(
                    name,
                    url=url
                )
                keyboard = InlineKeyboardMarkup([[button]])
                update.reply_text(f"Filtered message: {update.text}", reply_markup=keyboard)
                return


# Run the bot
app.run()
