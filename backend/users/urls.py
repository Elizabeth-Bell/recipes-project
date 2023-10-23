from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

app_name = 'users'

v1_router = DefaultRouter()

v1_router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
]
