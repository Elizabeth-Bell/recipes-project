import base64
from django.conf import settings
from django.shortcuts import get_object_or_404
import webcolors
from rest_framework import serializers

from django.core.files.base import ContentFile

from recipes.models import (Ingredient, Tag, Recipe,
                            FavoriteRecipe, RecipeIngredients,
                            RecipeTags,
                            ShoppingCart)
from users.models import CustomUser, Subscribe
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    """Сериализатор для кодирования/декодирования
    картинки с помощью base64.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' +ext)

        return super().to_internal_value(data)


class Hex2NameToColor(serializers.Field):
    """Поле для перевода HEX-кода цвета в название."""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Этого цвета нет в '
                                              'библиотеке цветов')
        return data


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра тэгов."""
    color = Hex2NameToColor(required=False)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления/просмотра ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения ингредиента."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления ингредиента в рецепт."""
    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.IntegerField(min_value=1, max_value=settings.MAX_VALIDATION)
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount', 'measurement_unit', 'name')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления рецепта."""
    ingredients = AddIngredientRecipeSerializer(many=True, source='recipeingredients_set')
    image = Base64ImageField(required=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients', 'tags', 'image',
                  'text', 'cooking_time', 'author')
        read_only_fields = ('author',)

    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredients_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            RecipeTags.objects.create(tag=tag, recipe=recipe)
        for ingredient in ingredients:
            pk = ingredient['ingredient']['id']
            amount = ingredient['amount']
            current_ingredient = Ingredient.objects.get(id=pk)
            RecipeIngredients.objects.create(ingredient_id=current_ingredient.id,
                                             recipe_id=recipe.id, amount=amount)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        if 'tags' in validated_data:
            instance.tags.clear()
            tags_data = validated_data.pop('tags')
            lst = []
            for tag in tags_data:
                lst.append(tag)
            instance.tags.set(lst)
        if 'recipeingredients_set' in validated_data:
            instance.ingredients.clear()
            ingredient_data = validated_data.pop('recipeingredients_set')
            for ingredient in ingredient_data:
                pk = ingredient['ingredient']['id']
                amount = ingredient['amount']
                current_ingredient = Ingredient.objects.get(id=pk)
                RecipeIngredients.objects.create(ingredient=current_ingredient,
                                                 amount=amount, recipe=instance)
        instance.save()
        return instance

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError('Время приготовления '
                                              'не может быть меньше минуты')
        return value


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения рецепта/списка рецептов."""
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredients_set')
    tags = TagSerializer(many=True)
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        recipe = obj.id
        user = self.context['request'].user.id
        return FavoriteRecipe.objects.filter(recipe=recipe, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        recipe = obj.id
        user = self.context['request'].user.id
        return ShoppingCart.objects.filter(recipe=recipe, user=user).exists()
