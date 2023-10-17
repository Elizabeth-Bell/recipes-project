from rest_framework import permissions

from users.models import CustomUser

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ на изменение/удаление объекта только для автора."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or any([obj.author == request.user,
                        request.user.is_staff,
                        request.user.is_superuser])
                )