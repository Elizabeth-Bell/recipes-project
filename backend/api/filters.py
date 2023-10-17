from rest_framework import filters
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    """Фильтр для поиска по ингредиентам."""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = '__all__'


class MyFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())

        return kwargs


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name='tags__slug')
    author = filters.CharFilter(field_name='author_id', lookup_expr='exact')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(fav_users__user_id=user.id)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(shop_users__user_id=user.id)
        return queryset
