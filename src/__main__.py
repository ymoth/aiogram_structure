"""
Run the main file
    > Connect the database, models and the necessary packages to run the bot itself.
    > Assigning the right middlewares
"""
import loguru
from aiogram import Bot
from aiogram.utils import executor
from tortoise import Tortoise

from src.middlewares import setup_middlewares
from src.misc import dispatcher, setup_logging


async def on_startup(bot: Bot):
    """
    Main launch function.
    Connecting logging, as well as connecting other dependencies and a database to run
    """
    get_a_dispatcher = await dispatcher.bot.get_me()

    setup_middlewares(dispatcher=dispatcher)
    setup_logging(bot_name=get_a_dispatcher['first_name'])

    loguru.logger.opt(colors=True).info(
        'Complete authorization, welcome {name} | <yellow>@{tag}</yellow>',
        name=get_a_dispatcher['first_name'], tag=get_a_dispatcher['username']
    )

    loguru.logger.info("Connecting database.. ")
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={"models": ["src.db_models"]},
        # timezone=tzlocal.get_localzone_name()
    )

    await Tortoise.generate_schemas()
    loguru.logger.success("Database success connected.")
    return None


async def on_shutdown(bot: Bot):
    await Tortoise.close_connections()
    loguru.logger.info('Success exit of bot')


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
