from recipes.models import RecipeIngredients, ShoppingCart


def add_to_favorite_or_shopping_cart(model, obj_id, model_through,
                                     user, serializer):
    """Функция добавления в избранное и корзину"""
    object = model.objects.get(id=obj_id)
    if not model_through.objects.filter(user=user,
                                        recipe=object).exists():
        model_through.objects.create(user=user,
                                     recipe=object)
        serializer = serializer(object)
        return serializer


def delete_from_favorite_or_shopping_cart(object, model_through, user):
    """Функция удаления из избранного и корзины"""
    if model_through.objects.filter(user=user,
                                    recipe=object).exists():
        favorite_obj = model_through.objects.get(
            user=user, recipe=object)
        favorite_obj.delete()
        return True
    return False


def get_unique_ingredients(request):
    """Функция формирования списка покупок."""
    shopping_cart = ShoppingCart.objects.filter(
        user=request.user).values_list('recipe_id', flat=True)
    ingredients = RecipeIngredients.objects.filter(
        recipe_id__in=shopping_cart).values_list(
        'ingredient__name',
        'amount',
        'ingredient__measurement_unit'
    )
    counted_ingredients = {}
    for name, amount, unit in ingredients:
        if name not in counted_ingredients:
            counted_ingredients[name] = amount, unit
        else:
            counted_ingredients[name] = (counted_ingredients[name][0]
                                         + amount, unit)
    shopping_list = ''
    for name, (amount, unit) in counted_ingredients.items():
        shopping_list += f'{name}: {amount} {unit}\n'
    return shopping_list
