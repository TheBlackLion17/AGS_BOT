# bot.py

from pyrogram import Client, filters
from config import Config
from pytz import timezone


# Initialize the Pyrogram Client
class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Agsmods",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN
        )

@Bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    print("bot has been started")

print("Bot Started")
# Start the Pyrogram Client
Bot().run()
