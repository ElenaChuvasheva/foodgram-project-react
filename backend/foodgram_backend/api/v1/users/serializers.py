from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import SerializerMethodField

from utils.calculations import is_subscribed

User = get_user_model()


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
            return None
        return is_subscribed(self.context['request'].user, obj)


class CustomUserSubscribeSerializer(CustomUserSerializer):
    pass
