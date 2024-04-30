import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Pyrogram client
app = Client("autofilter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Regular expression pattern to match the specified format with alphanumeric filter names
pattern = r"\[([a-zA-Z0-9]+)\]\(buttonurl://(.*?):(.*?)\)"

# Dictionary to store filter name and URL pairs
filters_dict = {}


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
        # Extract filter name, URL, and button text from the command
        match = re.match(pattern, text[1])
        if match:
            name = match.group(1)
            url = match.group(2)
            button_text = match.group(3)
            filters_dict[name] = {"url": url, "button_text": button_text}
            update.reply_text(f"Filter '{name}' added successfully!")
        else:
            update.reply_text("Invalid filter format. Please use [name](buttonurl://example.com:same) format with alphanumeric filter names.")
    else:
        update.reply_text("Please provide a filter in the correct format after the command.")


# Command to show filters to the user
@app.on_message(filters.command("showfilter") & filters.private)
def show_filter_command(_, update):
    if filters_dict:
        filters_info = "\n".join([f"- {name}: {data['url']}" for name, data in filters_dict.items()])
        update.reply_text(f"Current Filters:\n{filters_info}")
    else:
        update.reply_text("There are no filters currently.")


# Function to handle messages containing filter names
@app.on_message(~filters.private)
def handle_filter_name(_, update):
    # Check if the message contains the name of a filter
    for name in filters_dict.keys():
        if name.lower() in update.text.lower():
            # Send the corresponding filter to the user
            data = filters_dict[name]
            button = InlineKeyboardButton(data["button_text"], url=data["url"])
            keyboard = InlineKeyboardMarkup([[button]])
            update.reply_text(f"Filter '{name}': {data['button_text']}", reply_markup=keyboard)
            return


# Run the bot
app.run()
