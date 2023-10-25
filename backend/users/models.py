from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активный')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Администратор')
    is_superuser = models.BooleanField(default=False,
                                       verbose_name='Суперпользователь')
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z',
                                   message='Имя пользователя'
                                   'содержит недопустимые'
                                           'символы.'), ]
    )
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='email')
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия')
    password = models.CharField(max_length=150,
                                verbose_name='Пароль')
    date_joined = models.DateTimeField(
        verbose_name='Дата создания пользователя',
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        verbose_name='Последний вход в систему',
        auto_now=True
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_active


class Subscribe(models.Model):
    """Модель создания подписки на автора."""
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='authors')
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             verbose_name='Подписчик',
                             related_name='subscriber')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
