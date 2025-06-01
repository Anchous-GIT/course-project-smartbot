from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

from business.BusinessService import BusinessService
from database.Database import db
from enums.RequestEnum import RequestEnum

TYPE_REQUEST, TEXT_REQUEST = range(2)


def get_request_conversation_handler(business_service: BusinessService) -> ConversationHandler:
    async def start_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Регистрация заявки.")
        keyboard = [[r.value] for r in RequestEnum]
        await update.message.reply_text(
            "Выберите тип заявки:",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )
        return TYPE_REQUEST

    async def receive_request_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            request_type = RequestEnum(update.message.text)
        except ValueError:
            await update.message.reply_text("Неверный тип. Выберите снова:")
            return TYPE_REQUEST

        context.user_data["request_type"] = request_type
        await update.message.reply_text("Введите описание заявки:", reply_markup=ReplyKeyboardRemove())
        return TEXT_REQUEST

    async def save_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        telegram_id = update.effective_user.id
        user = db.get_user_by_telegram_id(telegram_id)
        request_type = context.user_data.get("request_type")

        try:
            business_service.request_svc.create_request(user, request_type, text)
        except Exception as e:
            await update.message.reply_text(f"Ошибка при создании заявки: {str(e)}")
            return ConversationHandler.END

        await update.message.reply_text("✅ Заявка успешно зарегистрирована.")
        return ConversationHandler.END

    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Заявка отменена.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    return ConversationHandler(
        entry_points=[CommandHandler("request", start_request)],
        states={
            TYPE_REQUEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_request_text)],
            TEXT_REQUEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_request)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
