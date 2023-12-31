import re

from django.core.exceptions import ValidationError


def validate_username(username):
    """Функция валидации юзернейма"""
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise ValidationError('"Имя пользователя" '
                              'содержит недопустимые символы')
