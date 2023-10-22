from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from django.http import HttpResponse

from recipes.models import Tag, Recipe, Ingredient, FavoriteRecipe, ShoppingCart, RecipeIngredients

from .serializers import (TagSerializer, RecipeSerializer, IngredientSerializer,
                          RecipeListSerializer)
from users.serializers import AddRecipeFavoriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from users.models import CustomUser


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
    permission_classes = IsAuthorOrReadOnly,

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
        if request.method == 'POST':
            if Recipe.objects.filter(id=recipe_id).exists():
                recipe = Recipe.objects.get(id=recipe_id)
                if not FavoriteRecipe.objects.filter(user=request.user,
                                                    recipe=recipe).exists():
                    FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
                    serializer = AddRecipeFavoriteSerializer(recipe)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if FavoriteRecipe.objects.filter(user=request.user, recipe=recipe).exists():
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
        if request.method == 'POST':
            if Recipe.objects.filter(id=recipe_id).exists():
                recipe = Recipe.objects.get(id=recipe_id)
                if not ShoppingCart.objects.filter(user=request.user,
                                                   recipe=recipe).exists():
                    ShoppingCart.objects.create(user=request.user, recipe=recipe)
                    serializer = AddRecipeFavoriteSerializer(recipe)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingCart.objects.filter(user=request.user, recipe=recipe).exists():
            shop_recipe = ShoppingCart.objects.get(user=request.user, recipe=recipe)
            shop_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated],
            url_path='download_shopping_cart')
    def get_shopping_list(self, request):
        shopping_cart = ShoppingCart.objects.filter(
            user=request.user).values_list('recipe_id', flat=True)
        ingredients = RecipeIngredients.objects.filter(
            recipe_id__in=shopping_cart).values_list('ingredient__name',
                                                     'amount',
                                                     'ingredient__measurement_unit')
        counted_ingredients = {}
        for name, amount, unit in ingredients:
            if name not in counted_ingredients:
                counted_ingredients[name] = amount, unit
            else:
                counted_ingredients[name] = (counted_ingredients[name][0] + amount, unit)
        shopping_list = ''
        for name, (amount, unit) in counted_ingredients.items():
            shopping_list += f'{name}: {amount} {unit}\n'
        file_name = f'{request.user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, headers={'Content-Type': 'text/plain',
                                'Content-disposition': f'attachment; filename={file_name}'})
        return response

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ВЬюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter
    filterset_fields = ('name',)


