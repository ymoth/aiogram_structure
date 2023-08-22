import dataclasses
import typing

from aiogram import types
from aiogram.dispatcher.filters import Filter

from src.db_models import Client
from src.permissions import Permissions


@dataclasses.dataclass
class PermissionFilter(Filter):
    """
    A filter for checking the desired permissions that you specify in the decorator.
    Example using:
    TODO:
        @dispatcher.message_handlers(Command("kick"), PermissionFilter(Permissions.ADMIN))
        async def some_function(context: types.Message, *your_args) -> your_type:
            pass
    """

    permission: typing.Union[Permissions, int]

    async def check(self, *args) -> bool:
        message: types.Message = args[0]
        user = await Client.get_or_none(telegram_id=message.from_user.id)

        permission = int(self.permission.value) if isinstance(self.permission, Permissions) else self.permission
        if user is not None and int(user.permission.value) >= permission:
            return True
        return False
