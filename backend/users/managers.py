from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер."""
    def create_user(self, email, username, first_name,
                    last_name, password=None):
        """Функция создания пользователя."""
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password,
                         first_name='super', last_name='user'):
        """Функция создания суперпользователя."""
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
