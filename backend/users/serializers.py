import re
from rest_framework import serializers

from .models import CustomUser, Subscribe


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для списка пользователей."""
    #is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')
                  #'is_subscribed')

    #def get_is_subscribed(self, obj):
        #subscribe = Subscribe.objects.get(user_id=self.id, author_id=obj.id)
        #return subscribe


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователей."""
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password',
                  'first_name', 'last_name')

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('Имя введено в некорректном формате')
        return value
