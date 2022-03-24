from telethon import TelegramClient
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

# Use your own values from my.telegram.org
api_id = 2309777
api_hash = 'e201aa5a789c6fc8e4998e83d9889681'


# The first parameter is the .session file name (absolute paths allowed)
# client = TelegramClient('nftalem', api_id, api_hash)
botClint = TelegramClient('bot', api_id, api_hash)

