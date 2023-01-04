from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import CharField, SerializerMethodField

from users.models import Subscribe

User = get_user_model()


def is_subscribed(obj1, obj2):
    return Subscribe.objects.filter(user=obj1, author=obj2).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request_user = self.context['request'].user
        if request_user.is_anonymous:
            return False
        return is_subscribed(self.context['request'].user, obj)


class CustomUserSubscribeSerializer(CustomUserSerializer):
    pass