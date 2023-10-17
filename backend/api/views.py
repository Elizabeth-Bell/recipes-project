from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from recipes.models import Tag, Recipe, Ingredient, FavoriteRecipe, ShoppingCart

from .serializers import (TagSerializer, RecipeSerializer, IngredientSerializer,
                          RecipeListSerializer)
from users.serializers import AddRecipeFavoriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ВЬюсет для тэгов только для чтения."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    filterset_fields = ('tags', 'author', 'is_favorited',
                        'is_in_shopping_cart')
    pagination_class = CustomPagination
    permission_class = IsAuthorOrReadOnly,

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated],
            url_path='(?P<recipe_id>[^/.]+)/favorite')
    def add_delete_favorite_recipe(self, request, recipe_id):
        """Функция добавления/удаления рецепта из избранного."""
        if Recipe.objects.filter(id=recipe_id).exists():
            recipe = Recipe.objects.get(id=recipe_id)
            if request.method == 'POST':
                if not FavoriteRecipe.objects.filter(user=request.user,
                                                     recipe=recipe).exists():
                    FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
                    serializer = AddRecipeFavoriteSerializer(recipe)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            recipe = Recipe.objects.get(id=recipe_id)
            favorite_recipe = FavoriteRecipe.objects.get(user=request.user, recipe=recipe)
            favorite_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated],
            url_path='(?P<recipe_id>[^/.]+)/shopping_cart')
    def add_delete_shopping_cart(self, request, recipe_id):
        """Функция добавления/удаления рецепта из списка покупок."""
        if Recipe.objects.filter(id=recipe_id).exists():
            recipe = Recipe.objects.get(id=recipe_id)
            if request.method == 'POST':
                if not ShoppingCart.objects.filter(user=request.user,
                                                   recipe=recipe).exists():
                    ShoppingCart.objects.create(user=request.user, recipe=recipe)
                    serializer = AddRecipeFavoriteSerializer(recipe)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            recipe = Recipe.objects.get(id=recipe_id)
            shop_recipe = ShoppingCart.objects.get(user=request.user, recipe=recipe)
            shop_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ВЬюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter
    filterset_fields = ('name',)

