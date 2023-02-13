from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from core import settings
from middlewares import setup as setup_middlewares

bot = Bot(settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# Setup middlewares
setup_middlewares(dp)
