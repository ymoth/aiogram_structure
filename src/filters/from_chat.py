from aiogram import types
from aiogram.dispatcher.filters import Filter


class FromChat(Filter):
    async def check(self, *args) -> bool:
        message: types.Message = args[0]

        if message.chat.type in (
                types.ChatType.GROUP,
                types.ChatType.CHANNEL,
                types.ChatType.SUPERGROUP
        ):
            return True
        return False
