from rest_framework import permissions


class IsMe(permissions.BasePermission):
    """Пермишен на доступ к эндпойнту users/me"""
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.id == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ на изменение/удаление объекта только для автора или админа."""
    def has_permission(self, request, view) -> bool:
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        return (request.method in permissions.SAFE_METHODS
                or any([obj.author == request.user,
                        request.user.is_staff,
                        request.user.is_superuser])
                )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ на удаление, удаление для админа."""
    def has_object_permission(self, request, view, obj) -> bool:
        return (request.method in permissions.SAFE_METHODS
                or any([request.user.is_staff,
                        request.user.is_superuser])
                )
