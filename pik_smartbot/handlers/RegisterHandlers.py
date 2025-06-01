from telegram.ext import Application

from business.BusinessService import BusinessService
from handlers.edit_profile import edit_profile_handler
from handlers.profile import get_profile_handler
from handlers.registration import get_register_conversation_handler
from handlers.request import get_request_conversation_handler


def register_all_handlers(app: Application, business_service: BusinessService):
    app.add_handler(get_register_conversation_handler(business_service))
    app.add_handler(get_profile_handler(business_service))
    app.add_handler(edit_profile_handler)
    app.add_handler(get_request_conversation_handler(business_service))