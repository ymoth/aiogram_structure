
### Aiogram Structure | Удобная структура для быстрого запуска<br>v: 1.0.0

## По вопросам, можете написать мне в телеграм:
 - https://t.me/pdxnz
# Установка
### Установка самого бота
Вы можете скачать проект с гитхаба, распаковав в удобную вам папку.

### Установка модулей
> Нужные нам модули: *(python -m pip install <module_name>)*
>> tortoise-orm<br>aiogram<br>loguru<br>
### Сам запуск проекта
- Зайдите в папку с проектом
- Измените ваш токен доступа для бота, на нужный в src.misc:8 $ACCESS_TOKEN
- Вернитесь обратно в корневую папку с проектом
- Выполните команду для запуска: __python -m src__

После успешного запуска должно отобразиться в консоли, по типу:
```sass
[04:02:02] >> Complete authorization, welcome <BOT_NAME> | @BOT_USERNAME
[04:02:02] >> Connecting database..                                    
[04:02:02] >> Database success connected.
```
# О структуризации
***
### SRC - Source
Структура основана на src пакете, в котором построены уже нужные зависимости и фаст старт для вас с удобным логгингом и обработкой нужных пакетов. Инициализируется всё в одном пакете __init__.
Сама структура описывается таким образом:<br>
 > PROJECT_NAME
 >> src
 >>>> - db_models<br>- client.py
 >>> - filters
 >>>> handlers
 >>>> - chat_handlers
 >>>> - local_handlers -> on_start.py
 >>> - middlewares
 >>> - misc.py
 >>> - permissions.py
 >>> - main.py
 >>> - init.py
***
### db_models - Модели базы данных.
Модель *Client* уже находится в нужной части кода, вы её можете рефакторить под себя, ознакомьтесь со статьей о tortoise-orm
https://tortoise.github.io/
```python
class Client(tortoise.Model):
    """
    The main user model, where the fields
    for the database are registered: db.sqlite3.
    In this model, the main role of the user and his further actions are formed.
    """

    id: int

    telegram_id = fields.IntField(description="Telegram user id")
```
***
### Filters - фильтры и обработчики событий
Сами фильтры лежат в src.filters, в принципе сам готовый реализованный пример в части кода:
Данные фильтры уже были созданы: 
> FromChat<br>FromLocal<br>PermissionFilter

```python
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
```
***
### Handlers - обработчики событий
Сами обработчики событий находятся в src.handlers папке. После чего, можно их добавлять, но не забудьте использовать нужные фильтры и само импортирование нужного пакета в 
```python
__init__.py
> from . import your_package_name
> from . import your_package_name2
> from . import your_package_name3

```
Пример создания обработчика.
```python
@dispatcher.message_handler(
    Command("test"),
    PermissionFilter(permission=Permissions.DEFAULT),
    PermissionFilter(permission=Permissions.SUPPORT)
)
async def permission_test_command(context: types.Message):
    user = await Client.get_or_none(telegram_id=context.from_user.id)
    await context.reply(f"Успешно пройдена проверка ранга. Ваш ранг: {user.get_permission_name_or_attr()}")
```