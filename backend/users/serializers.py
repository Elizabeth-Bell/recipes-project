import re

from recipes.models import Recipe
from rest_framework import serializers

from .models import CustomUser, Subscribe


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для списка пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        """Функция получения значения поля 'Подписка'."""
        user = self.context['request'].user.id
        author = obj.id
        return Subscribe.objects.filter(user_id=user,
                                        author_id=author).exists()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователей."""
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name')

    def validate_username(self, value):
        """Валидация юзернейма."""
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'Имя введено в некорректном формате'
            )
        return value


class AddRecipeFavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для рецепта с урезанными полями для избранного."""
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeUserRecipe(serializers.ModelSerializer):
    """Сериалайзер пользователя для подписки/отписки."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        model = CustomUser

    def get_is_subscribed(self, obj):
        """Получение значения поля 'Вы подписаны'."""
        user = self.context['request'].user.id
        return Subscribe.objects.filter(user=user, author=obj.id).exists()

    def get_recipes(self, obj):
        """Получения поля рецептов в подписках."""
        request = self.context['request']
        recipe_limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.id)
        if recipe_limit:
            recipes = recipes[:int(recipe_limit)]
        serializer = AddRecipeFavoriteSerializer(recipes,
                                                 many=True,
                                                 read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """Получение значения поля общее кол-во рецептов польз-ля."""
        author = obj.id
        recipes = Recipe.objects.filter(author=author)
        return len(recipes)
