# smart_bot.py
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import logging

logger = logging.getLogger(__name__)

class SmartBot:
    def __init__(self, token: str):
        self.app: Application = ApplicationBuilder().token(token).build()

        # future: self.user_service = build_user_service()

        self._register_handlers()

    def _register_handlers(self):
        # Пока что только заглушка
        self.app.add_handler(CommandHandler("start", self._start_command))

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("👋 Hello! I'm SmartBot")

    def run(self):
        logger.info("SmartBot is starting...")
        self.app.run_polling()
