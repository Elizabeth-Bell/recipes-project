from django.contrib import admin

from .models import (Recipe,
                     Ingredient,
                     Tag,
                     FavoriteRecipe,
                     ShoppingCart)


class RecipeInline(admin.TabularInline):
    """Добавление ингредиентов в рецепт."""
    model = Recipe.ingredients.through


class RecipeTagsInline(admin.TabularInline):
    """Добавление тэгов в рецепт."""
    model = Recipe.tags.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админ-панель тэгов."""
    list_display = ('name', 'slug', 'color')
    search_field = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админ-панель ингредиентов."""
    list_display = ('name', 'measurement_unit')
    search_field = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ-панель рецептов."""
    list_display = ('name', 'author')
    search_field = ('name', 'tags', 'author')
    list_filter = ('name', 'tags', 'author')
    readonly_fields = ('in_favorite', )
    empty_value_display = '-пусто-'
    inlines = (
        RecipeInline,
        RecipeTagsInline,
    )


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Админ-панель избранных рецептов."""
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админ-панель рецептов в корзине."""
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'
