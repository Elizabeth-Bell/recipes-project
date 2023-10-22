from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import (filters, pagination, permissions, status,
                            viewsets)
from rest_framework.response import Response

from users.models import CustomUser, Subscribe
from users.serializers import UserSerializer, SubscribeUserRecipe
from api.pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly, IsMe
from djoser.serializers import UserCreateSerializer, SetPasswordSerializer, TokenSerializer, TokenCreateSerializer
from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):
    """ВЬюсет для пользователей."""
    queryset = CustomUser.objects.all()
    http_method_names = ['get', 'post', 'delete']
    pagination_class = CustomPagination

    @action(detail=False,
            permission_classes=[IsMe,],
            methods=['get', 'delete'])
    def me(self, request):
        me = get_object_or_404(CustomUser, id=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(me, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            me.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated],
            methods=['post', 'delete'], url_path='subscribe')
    def add_delete_subscribe(self, request, id=None):
        """Функция подписки/отписки от автора."""
        author = get_object_or_404(CustomUser, id=id)
        if request.method == 'POST':
            if not Subscribe.objects.filter(user=request.user,
                                            author=author).exists() and (
                    author != request.user):
                Subscribe.objects.create(user=request.user, author=author)
                serializer = SubscribeUserRecipe(author, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if Subscribe.objects.filter(user=request.user, author=author).exists():
            subscribe = Subscribe.objects.get(user=request.user, author=author)
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated],
            url_path='subscriptions')
    def get_subscriptions(self, request):
        """Функция списка подписок."""
        user = request.user
        subscriptions = CustomUser.objects.filter(authors__user=user.id)
        paginated_subs = self.paginate_queryset(subscriptions)
        if paginated_subs is not None:
            serializer = SubscribeUserRecipe(paginated_subs, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeUserRecipe(paginated_subs, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data, status=status.HTTP_200_OK)
