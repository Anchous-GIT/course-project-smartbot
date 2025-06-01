import asyncio

from telegram.ext import ApplicationBuilder

import config
from business.BusinessService import BusinessService
from handlers.RegisterHandlers import register_all_handlers
from services.UserService import UserService
from services.RequestService import RequestService
from services.DepartamentService import DepartamentService
from services.AccessControlService import AccessControlService


def main():
    app = ApplicationBuilder().token("8101451994:AAH62ZFSwJihwucdpkSz29U5McKLAs9Oznw").build()
    business_service = BusinessService(
        user_svc=UserService(),
        request_svc=RequestService(),
        department_svc=DepartamentService(),
        acs_svc=AccessControlService()
    )
    app.bot_data["business_service"] = business_service
    register_all_handlers(app, business_service)
    app.run_polling()

if __name__ == "__main__":
    main()
