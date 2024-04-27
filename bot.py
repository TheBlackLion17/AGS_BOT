# bot.py

from pyrogram import Client, filters
from config import Config
from pytz import timezone
# Replace these placeholders with your actual values

LOG_CHANNEL = -1002016756529  # Replace with your log channel ID

# Initialize the Pyrogram Client
class app(Client):
    def __init__(self):
        super().__init__(
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**{me.mention} Is Restarted !!**\n\n📅 Date : `{date}`\n⏰ Time : `{time}`\n🌐 Timezone : `Asia/Kolkata`\n\n🉐 Version : `v{__version__} (Layer {layer})`</b>")                                
            except:
                print("Please Make This Is Admin In Your Log Channel")

# Start the Pyrogram Client
app.run()
