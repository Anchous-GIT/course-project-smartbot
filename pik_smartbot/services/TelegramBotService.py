
import logging
from dataclasses import dataclass, field
from logging import Logger
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


@dataclass
class TelegramBotService:
    token: str
    smart_bot: 'SmartBotService'
    application: Application = field(init=False)
    logger: Logger = field(init=False)

    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("TelegramBotService was initialized")

        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()

    def setup_handlers(self) -> None:
        """Register bot commands with their handlers."""
        self.application.add_handler(CommandHandler("start", self.handle_start))
        self.application.add_handler(CommandHandler("help", self.handle_help))
        self.application.add_handler(CommandHandler("info", self.handle_info))
        self.application.add_handler(CommandHandler("request", self.handle_request))
        self.application.add_handler(CommandHandler("cancel", self.handle_cancel))

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Привет! Я SmartBot. Готов к работе 💼")
