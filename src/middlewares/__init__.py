from aiogram import Dispatcher

from src.middlewares.check_ban_middleware import IsBannedUser


def setup_middlewares(dispatcher: Dispatcher) -> None:
    """
    Middleware is an event handler, before the decorators themselves are processed.
    Until the middleware you need is executed,
        > the decorator will not be executed (the processing of the desired command itself)
    :param dispatcher: type[Dispatcher]
    :return: None
    """
    dispatcher.middleware.setup(IsBannedUser())
    return None
