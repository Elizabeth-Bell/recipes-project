import re

from django.core.exceptions import ValidationError


def validate_username(username):
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise ValidationError('"Имя пользователя" '
                              'содержит недопустимые символы')
