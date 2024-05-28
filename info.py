import re, time
from os import environ
from Script import script 

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]: return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]: return False
    else: return default


API_ID = int(environ('API_ID','6976445947'))
API_HASH = environ('API_HASH','d39c4324a40a8a6b27a067f8ff2b987e')
BOT_TOKEN = environ('BOT_TOKEN','7101381082:AAFOaYNVIksYKcRyEzbZ5Aa8Xrh4UwnE-K8')

WEBHOOK = bool(environ.get("WEBHOOK", True)) # for web support on/off
PICS = (environ.get('PICS' ,'https://telegra.ph/file/240720bec6145bb269f17.jpg')).split()
UPTIME = time.time()
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', "-1002128069308"))
