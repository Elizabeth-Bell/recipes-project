from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, RecipeViewSet, IngredientViewSet)

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'tags', TagViewSet)
v1_router.register(r'ingredients', IngredientViewSet)
v1_router.register(r'recipes', RecipeViewSet)


urlpatterns = [
    path('', include(v1_router.urls)),
]