import os, re, json, base64, logging, random, asyncio

from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import *

BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [
                InlineKeyboardButton('🔔 Updates 🤖', url='https://t.me/AgsModsOG')
            ],
            [
                InlineKeyboardButton('🙆🏻 Help 🦾', url=f"https://t.me/{temp.U_NAME}?start=help"),
            ],[
            InlineKeyboardButton('⪦ BOT Chat ⪧', url='https://t.me/ags_disscussion')
            ],
            [
                InlineKeyboardButton(text=DOWNLOAD_TEXT_NAME,url=DOWNLOAD_TEXT_URL)
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
        await asyncio.sleep(2) 
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('➕↖️ Add Me To Your Groups ↗️➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('🧞‍♀️ Search 🧐', switch_inline_query_current_chat=''),
            InlineKeyboardButton('🔔 Updates 🤖', url='https://t.me/AgsModsOG')
            ],[
            InlineKeyboardButton('🙆🏻 Help 🦾', callback_data='help'),
            InlineKeyboardButton('♥️ About ♥️', callback_data='about')
            ],[
            InlineKeyboardButton('🔗 More Help', callback_data='leech_url_help'),
            InlineKeyboardButton('⚙ Open Settings', callback_data='openSettings'),
            ],[
            InlineKeyboardButton('⪦ BOT Chat ⪧', url='https://t.me/ags_disscussion')
            ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
