import sys

import aiogram
import loguru
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = aiogram.Bot(token="$ACCESS_TOKEN")
dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())


def setup_logging(bot_name: str) -> None:
    loguru.logger.remove()
    loguru.logger.add(sys.stdout, format="<b><m>[{time:HH:mm:ss}]</m></b> >> <level>{message}</level>", level="INFO")

    loguru.logger.level("ERROR", color="<red><b>")
    loguru.logger.level("WARNING", color="<yellow><b>")
    loguru.logger.level("SUCCESS", color="<green><b>")
    loguru.logger.level("INFO", color="<blue><b>")
    return None
