from rest_framework import permissions

from users.models import CustomUser


class IsMe(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ на изменение/удаление объекта только для автора."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or any([obj.author == request.user,
                        request.user.is_staff,
                        request.user.is_superuser])
                )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ на удаление, удаление для админа."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or any([request.user.is_staff,
                        request.user.is_superuser])
                )
