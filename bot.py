from pyrogram import Client, filters

from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Pyrogram client
app = Client("autofilter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Command to start the bot
@app.on_message(filters.command("start"))
def start(_, update):
    update.reply_text("Hello! I'm an auto-filter bot. Send me a message and I'll filter it for you.")


# Auto-filter function
@app.on_message(~filters.command & ~filters.private)
def auto_filter(_, update):
    # You can add your filtering logic here
    # For this example, let's simply echo the message back
    update.reply_text(f"You sent: {update.text}")


# Run the bot
app.run()
