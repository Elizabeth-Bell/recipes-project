from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'users'

v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
]