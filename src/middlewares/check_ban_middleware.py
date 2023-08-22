import typing

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.db_models import Client


class IsBannedUser(BaseMiddleware):
    """
    Middleware of check the banned user
    """

    banned_message = (
        "Вы заблокированы в боте\n"
        "Что-бы разблокировать, отпишите администратору. "
    )

    async def on_process_message(self, message: types.Message, data: dict) -> typing.NoReturn:
        """
        This handler is called when dispatcher receives a message

        :param data:
        :param message:
        """

        user = await Client.get_or_none(telegram_id=message.from_user.id)
        if user is not None and user.is_banned:
            await message.answer(self.banned_message)
            raise CancelHandler()

    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict) -> typing.NoReturn:
        user = await Client.get_or_none(telegram_id=callback.from_user.id)
        if user is not None and user.is_banned:
            await callback.message.answer(self.banned_message)
            raise CancelHandler()

