from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import (filters, pagination, permissions, status,
                            viewsets)
from rest_framework.response import Response

from .models import CustomUser, Subscribe
from .serializers import UserSerializer, SignUpSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action == 'create':
            return SignUpSerializer
        return UserSerializer

#class SubscribesViewSet(viewsets.ModelViewSet):
    #serializer_class = UserSerializers

    #def get_queryset(self):
        #user =




#@api_view(['POST', 'DELETE'])
#def subscribe(request):
    #if request.method == 'GET':
        #authors = CustomUser.objects.all()
        #serializer = UserSerializers()
