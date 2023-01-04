from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.v1.users.serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.current_user
        return super().get_permissions()

# функция рабочая, но нужен отдельный view в recipes
#    @action(detail=False)
#    def my_subscriptions(self, request):
#        current_user = self.request.user
#        authors = User.objects.filter(subscribers__user=current_user)
#        page = self.paginate_queryset(authors)
#        serializer = CustomUserSubscribeSerializer(
#            page, many=True, context={'request': self.request})
#        return self.get_paginated_response(serializer.data)

#    @action(detail=True)
#    def subscribe(self, request, id):
#        return Response(f'{id} post', status=status.HTTP_200_OK)

#    @action(detail=True)
#    def unsubscribe(self, request, id):
#        return Response(f'{id} delete', status=status.HTTP_200_OK)

#class SubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
# class SubscriptionViewSet(viewsets.ModelViewSet):
#    serializer_class = CustomUserSerializer
#    def get_queryset(self):
#        current_user = self.request.user
#        return User.objects.filter(subscribers__user=current_user)

# предотвратить подписку на себя! делать класс не здесь
#    @action(detail=True, url_path='wtf', url_name='wtf', methods=['POST', 'DELETE'])
#    def my_subscriptions(self, request, pk):
#        authors = request.user.subscribed_to.all()
#        serializer = CustomUserSubscribeSerializer(authors, many=True)
#        return Response("wtf", status=status.HTTP_200_OK)
