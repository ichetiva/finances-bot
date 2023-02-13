from aiogram import Dispatcher

from .services_middleware import ServicesMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ServicesMiddleware())
