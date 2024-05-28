import re, time
from os import environ
from Script import script 

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]: return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]: return False
    else: return default


API_ID = int(environ('API_ID','20919286'))
API_HASH = environ('API_HASH','57b85f72104db3f08f9795b0410eb556')
BOT_TOKEN = environ('BOT_TOKEN','6900955318:AAFW2S6dhijU5ybVSH9qoPi-xucjBqDTqzE')

WEBHOOK = bool(environ.get("WEBHOOK", True)) # for web support on/off
PICS = (environ.get('PICS' ,'https://telegra.ph/file/240720bec6145bb269f17.jpg')).split()
UPTIME = time.time()
