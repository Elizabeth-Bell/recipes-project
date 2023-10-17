from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import (filters, pagination, permissions, status,
                            viewsets)
from rest_framework.response import Response

from users.models import CustomUser, Subscribe
from users.serializers import UserSerializer, SignUpSerializer, SubscribeUserRecipe
from api.pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAuthorOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """ВЬюсет для пользователей."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'delete']
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return SignUpSerializer
        return UserSerializer

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated],
            methods=['post', 'delete'], url_path='subscribe')
    def add_delete_subscribe(self, request, pk=None):
        """Функция подписки/отписки от автора."""
        author = get_object_or_404(CustomUser, id=pk)
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
