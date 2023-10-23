from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/', include('users.urls')),
    path(r'api/auth/', include('djoser.urls.authtoken')),
    path(r'api/', include('api.urls')),
]
