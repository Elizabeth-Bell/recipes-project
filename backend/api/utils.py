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
