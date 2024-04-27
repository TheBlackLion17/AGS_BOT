from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from config import Config, Txt 


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton('♨️ Updates', url='https://t.me/AgsModsOG'),
        InlineKeyboardButton('⭕️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/AgsModsOG')],
    [InlineKeyboardButton("👨‍💻 Developer", url='https://t.me/Agsmod')]
    ])
