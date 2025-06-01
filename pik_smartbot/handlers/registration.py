from datetime import datetime

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)
from business.BusinessService import BusinessService
from enums.CitizenshipEnum import CitizenshipEnum
from validation.registration import validate_full_name, validate_birth_date, validate_citizenship

# Состояния диалога
FULL_NAME, BIRTH_DATE, CITIZENSHIP = range(3)

def get_register_conversation_handler(business_service: BusinessService) -> ConversationHandler:

    async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Введите ваше имя")
        return FULL_NAME

    async def ask_birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        full_name = update.message.text
        is_valid, error = validate_full_name(full_name)
        if not is_valid:
            await update.message.reply_text(error+ "Попробуйте еще раз:")
            return FULL_NAME

        context.user_data["full_name"] = update.message.text
        await update.message.reply_text("Введите дату рождения в формате ДД.ММ.ГГГГ:")
        return BIRTH_DATE

    async def ask_citizenship(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        birth_date = update.message.text
        is_valid, error = validate_birth_date(birth_date)
        if not is_valid:
            await update.message.reply_text(error + "Попробуйте еще раз:")
            return BIRTH_DATE

        birth_date = datetime.strptime(birth_date, "%d.%m.%Y")
        context.user_data["birth_date"] = birth_date


        keyboard = [[c.value] for c in CitizenshipEnum]
        await update.message.reply_text(
            "Выберите гражданство:",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )
        return CITIZENSHIP


    async def complete_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        citizenship_input = update.message.text
        is_valid, error = validate_citizenship(citizenship_input)
        if not is_valid:
            await update.message.reply_text(error + "Повторите выбор:")
            return CITIZENSHIP

        citizenship = CitizenshipEnum(citizenship_input)
        telegram_id = update.effective_user.id
        full_name = context.user_data["full_name"]
        birth_date = context.user_data["birth_date"]

        try:
            user = business_service.register_user(
                telegram_id=telegram_id,
                full_name=full_name,
                birth_date=birth_date,
                citizenship=citizenship
            )
        except ValueError as e:
            await update.message.reply_text(
                f"Ошибка при регистрации: {str(e)}")
            return ConversationHandler.END


        await update.message.reply_text(f"✅ Пользователь {user.full_name} зарегистрирован.")
        return ConversationHandler.END

    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Регистрация отменена.")
        return ConversationHandler.END

    return ConversationHandler(
        entry_points=[CommandHandler("register", start_registration)],
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_birth_date)],
            BIRTH_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_citizenship)],
            CITIZENSHIP: [MessageHandler(filters.TEXT & ~filters.COMMAND, complete_registration)],
        },
            fallbacks=[CommandHandler("cancel", cancel)],
    )