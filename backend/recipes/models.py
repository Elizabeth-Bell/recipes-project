from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models

from colorfield.fields import ColorField

from users.models import CustomUser


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(verbose_name='Название ингредиента',
                            max_length=200)
    measurement_unit = models.CharField(verbose_name='Единицы измерения',
                                        max_length=200
                                        )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [models.UniqueConstraint(
            fields=['name', 'measurement_unit'],
            name='unique_ingredient'
        )
        ]

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """Модель тэга"""
    name = models.CharField(verbose_name='Название тега',
                            max_length=200)
    color = ColorField(verbose_name='Цвет',
                       max_length=7,
                       blank=True)
    slug = models.SlugField(verbose_name='Слаг',
                            validators=[RegexValidator(
                                regex=r'^[-a-zA-Z0-9_]+$',
                                message='Слаг содержит '
                                        'недопустимые символы'), ],
                            max_length=200,
                            unique=True,
                            blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredients',
                                         verbose_name='Ингрeдиенты',
                                         related_name='recipe')
    tags = models.ManyToManyField(Tag, through='RecipeTags',
                                  verbose_name='Тэги')
    image = models.ImageField(upload_to='recipes/images/',
                              default=None,
                              verbose_name='Фото блюда',
                              )
    name = models.CharField(verbose_name='Название блюда',
                            max_length=200)
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(verbose_name='Время приготовления'
                                                    'в минутах')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               verbose_name='Автор', related_name='recipes')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.name

    @admin.display(description='В избранном')
    def in_favorite(self) -> int:
        return len(FavoriteRecipe.objects.filter(recipe=self.id))


class RecipeIngredients(models.Model):
    """Модель для связанной таблицы рецептов и ингредиентов с количеством"""
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   related_name='recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    amount = models.IntegerField(verbose_name='Количество')

    def __str__(self) -> str:
        return f'{self.ingredient} {self.amount}'


class RecipeTags(models.Model):
    """Модель для связанной таблицы рецептов и тэгов."""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            verbose_name='Тэг')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    def __str__(self) -> str:
        return f'{self.recipe}{self.tag}'


class FavoriteRecipe(models.Model):
    """Модель для избранных рецептов"""
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='fav_recipes')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='fav_users')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    """Модель для корзины покупок."""
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='shop_recipes')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт в корзине',
                               related_name='shop_users')

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
