from telegram import Update
from telegram.ext import ContextTypes

from business.BusinessService import BusinessService


def get_handler(business_service: BusinessService):
    async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"👋 Привет, {user.first_name}! Добро пожаловать!"
        )

    return start_handler()
