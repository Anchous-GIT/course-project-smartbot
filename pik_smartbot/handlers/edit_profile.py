from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

from business.BusinessService import BusinessService
from classes.User import User
from database.Database import db
from validation.registration import (
    validate_full_name, validate_birth_date, validate_citizenship,
    validate_department, validate_workstation,
    validate_role, validate_position
)

CHOOSING_FIELD, EDITING_FIELD = range(2)


FIELD_VALIDATORS = {
    "ФИО": validate_full_name,
    "Дата рождения": validate_birth_date,
    "Гражданство": validate_citizenship,
    "Отдел": validate_department,
    "Рабочее место": validate_workstation,
    "Роль": validate_role,
    "Должность": validate_position
}

FIELD_ATTRS = {
    "ФИО": "full_name",
    "Дата рождения": "birth_date",
    "Гражданство": "citizenship",
    "Отдел": "department",
    "Рабочее место": "workstation_number",
    "Роль": "role",
    "Должность": "position"
}


async def start_edit_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["ФИО", "Дата рождения"],
        ["Гражданство", "Отдел"],
        ["Рабочее место", "Роль", "Должность"],
        ["Завершить редактирование"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Что вы хотите изменить в профиле?", reply_markup=reply_markup)
    return CHOOSING_FIELD


async def choose_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    field = update.message.text
    if field == "Завершить редактирование":
        return await confirm_finish(update, context)

    if field not in FIELD_VALIDATORS:
        await update.message.reply_text("Неизвестное поле. Выберите из клавиатуры.")
        return CHOOSING_FIELD

    context.user_data["edit_field"] = field
    await update.message.reply_text(f"Введите новое значение для поля: {field}")
    return EDITING_FIELD


async def process_new_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = update.message.text
    field = context.user_data.get("edit_field")

    validator = FIELD_VALIDATORS.get(field)
    if not validator:
        await update.message.reply_text("Что-то пошло не так. Попробуйте ещё раз.")
        return CHOOSING_FIELD

    is_valid, result = validator(value)
    if not is_valid:
        await update.message.reply_text(result + "\nПопробуйте ещё раз:")
        return EDITING_FIELD

    context.user_data[f"new_{field}"] = result
    await update.message.reply_text(
        f"Поле '{field}' успешно обновлено.\nХотите изменить что-то ещё?",
    )
    return CHOOSING_FIELD

async def confirm_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем бизнес-сервис из глобального контекста
    business_service: BusinessService = context.bot_data.get("business_service")
    if not business_service:
        await update.message.reply_text("❌ Внутренняя ошибка: сервисы недоступны.")
        return ConversationHandler.END

    telegram_id = update.effective_user.id
    user = db.get_user_by_telegram_id(telegram_id)


    if not user or not isinstance(user, User):
        await update.message.reply_text("❌ Ошибка: пользователь не найден. Пройдите регистрацию.")
        return ConversationHandler.END

    updates = {
        FIELD_ATTRS[field]: value
        for key, value in context.user_data.items()
        if key.startswith("new_")
        for field in [key.replace("new_", "")]
    }

    if not updates:
        await update.message.reply_text(
            "Вы не внесли никаких изменений.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    try:
        business_service.update_user_profile(user.id, updates)
        await update.message.reply_text(
            "✅ Изменения профиля сохранены.",
            reply_markup=ReplyKeyboardRemove()
        )
    except ValueError as e:
        await update.message.reply_text(
            f"Произошла ошибка при сохранении изменений: {str(e)}",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        # Любая другая непредвиденная ошибка
        await update.message.reply_text(
            f"⚠️ Системная ошибка при сохранении: {e}",
            reply_markup=ReplyKeyboardRemove()
        )
    context.user_data.clear()
    return ConversationHandler.END


async def cancel_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Редактирование отменено.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


edit_profile_handler = ConversationHandler(
    entry_points=[CommandHandler("edit_profile", start_edit_profile)],
    states={
        CHOOSING_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_field)],
        EDITING_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_new_value)],
    },
    fallbacks=[CommandHandler("cancel", cancel_edit)],
)
