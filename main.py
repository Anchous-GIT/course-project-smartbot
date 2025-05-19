# main.py
import logging
from smart_bot import SmartBot

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    bot = SmartBot(BOT_TOKEN)
    bot.run()
