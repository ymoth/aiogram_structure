from datetime import datetime

import tortoise
from tortoise import fields
from tortoise.fields import ForeignKeyRelation, ForeignKeyField

from src.permissions import Permissions, PERMISSION_NAMES


class _BaseControlTime:
    id = tortoise.fields.IntField(pk=True)

    start_time: datetime = tortoise.fields.DatetimeField(auto_now=True, )
    end_time: datetime = tortoise.fields.DatetimeField()

    description: str = tortoise.fields.TextField()
    is_closed = tortoise.fields.BooleanField(default=False)

    user: ForeignKeyRelation['Client']


class BanClient(_BaseControlTime, tortoise.Model):
    user: ForeignKeyRelation['Client'] = ForeignKeyField('db_models.Client', related_name='bans')


class WarnClient(_BaseControlTime, tortoise.Model):
    user: ForeignKeyRelation['Client'] = ForeignKeyField('db_models.Client', related_name='warns')


class Client(tortoise.Model):
    """
    The main user model, where the fields
    for the database are registered: db.sqlite3.
    In this model, the main role of the user and his further actions are formed.
    """

    id: int

    telegram_id = fields.IntField(description="Telegram user id")
    username = fields.CharField(default=None, null=True, max_length=30)

    permission = fields.CharEnumField(Permissions)

    is_banned = fields.BooleanField(default=False)

    bans = tortoise.fields.ReverseRelation['BanClient']
    warns = tortoise.fields.ReverseRelation['WarnClient']

    def get_permission_name_or_attr(self, attr: str = None):
        return PERMISSION_NAMES[int(self.permission.value)][attr or "name"]

    def get_permission_data(self):
        return PERMISSION_NAMES[int(self.permission.value)]
