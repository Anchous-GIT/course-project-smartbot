from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from business.BusinessService import BusinessService

def get_profile_handler(business_service: BusinessService) -> CommandHandler:
    async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            profile_data = business_service.get_profile_data(update.effective_user.id)
            await update.message.reply_text(profile_data, parse_mode="Markdown")
        except ValueError as e:
            await update.message.reply_text(str(e))

    return CommandHandler("profile", show_profile)
