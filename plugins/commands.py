import os, re, json, base64, logging, random, asyncio

from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import *

BATCH_FILES = {}

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await roheshbots.add_user(client, message)                
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton('♨️ Updates', url='https://t.me/AgsModsOG'),
        InlineKeyboardButton('⭕️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/AgsModsOG')],
        [InlineKeyboardButton('💢 About', callback_data='about'),
        InlineKeyboardButton('🥹 Help', callback_data='help')],
        [InlineKeyboardButton("👨‍💻 Developer", url='https://t.me/Agsmod')]
    ])
    if PIC:
        await message.reply_photo(PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)
   

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('♨️ Updates', url='https://t.me/AgsModsOG'),
                InlineKeyboardButton('⭕️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/AgsModsOG')],
                [InlineKeyboardButton('💢 About', callback_data='about'),
                InlineKeyboardButton('🥹 Help', callback_data='help')],
                [InlineKeyboardButton("👨‍💻 Developer", url='https://t.me/Agsmod')]
            ])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚡ 4GB Rename Bot", url="https://t.me/AgsModsOG")],
                [InlineKeyboardButton("🔒 Close", callback_data = "close"),
                InlineKeyboardButton("◀️ Back", callback_data = "start")]
            ])            
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 More Bots", url="https://t.me/AgsModsOG")],
                [InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data = "start")]
            ])            
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
