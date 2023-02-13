from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from db import async_session
from services import ServicesFactory


class ServicesMiddleware(LifetimeControllerMiddleware):
    async def pre_process(self, obj, data, *args):
        data["session"] = async_session()
        data["services"] = ServicesFactory(data["session"])
    
    async def post_process(self, obj, data, *args):
        await data["session"].close()
        del data["session"]
