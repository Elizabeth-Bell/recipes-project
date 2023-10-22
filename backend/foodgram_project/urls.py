from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/', include('users.urls')),
    path(r'api/auth/', include('djoser.urls.authtoken')),
    path(r'api/', include('api.urls')),
]

#handler404 = 'api.views.page_not_found'

#Нужные эндпойнты из djoser
#/users/
#/users/me/
#/users/set_password/
#/users/reset_password/
#/token/login/
#/token/logout/