from django.contrib import admin

from .models import Recipe, RecipeIngredients, Ingredient, Tag, RecipeTags


class RecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through

class RecipeTagsInline(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_field = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_field = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'text', 'cooking_time', 'author')
    search_field = ('name', 'tags')
    list_filter = ('name', 'tags')
    empty_value_display = '-пусто-'
    inlines = [
        RecipeInline,
        RecipeTagsInline,
    ]