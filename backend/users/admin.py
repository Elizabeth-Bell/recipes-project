from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subscribe


class UserAdminModel(UserAdmin):
    readonly_fields = ['date_joined', 'last_login']



admin.site.register(CustomUser,UserAdminModel)

admin.site.register(Subscribe)