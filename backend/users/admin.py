from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subscribe


class UserAdminModel(UserAdmin):
    readonly_fields = ['date_joined', 'last_login']


@admin.register(CustomUser)
class UserAdmin(UserAdminModel):
    """Админ-панель пользователей."""
    list_display = ('username', 'email',
                    'first_name', 'last_name')
    search_field = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


@admin.register(Subscribe)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админ-панель подписок."""
    list_display = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'
