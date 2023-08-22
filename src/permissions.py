import enum

PERMISSION_NAMES = {
    0: {"name": "Пользователь"},
    500: {"name": "Агент"},
    1000: {"name": "Администратор"}
}


class Permissions(enum.Enum):
    """
    Separated class of users by access levels to commands
    """

    DEFAULT = '0'
    SUPPORT = '500'
    ADMIN = '1000'
