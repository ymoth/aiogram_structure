from aiogram import types
from aiogram.dispatcher.filters import Command

from src.db_models import Client
from src.filters import PermissionFilter
from src.misc import dispatcher
from src.permissions import Permissions


@dispatcher.message_handler(Command("start"))
async def on_start(context: types.Message):
    user = await Client.get_or_none(telegram_id=context.from_user.id)
    if user is None:
        user = await Client.create(
            telegram_id=context.from_user.id,
            username=context.from_user.username,
            permission=Permissions.DEFAULT
        )

    await context.reply(f"Welcome, {user.username}. ")


@dispatcher.message_handler(
    Command("test"),
    PermissionFilter(permission=Permissions.DEFAULT),
    PermissionFilter(permission=Permissions.SUPPORT)
)
async def permission_test_command(context: types.Message):
    user = await Client.get_or_none(telegram_id=context.from_user.id)
    await context.reply(f"Успешно пройдена проверка ранга. Ваш ранг: {user.get_permission_name_or_attr()}")
