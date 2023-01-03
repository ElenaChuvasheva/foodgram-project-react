from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.users.serializers import CustomUserSubscribeSerializer
from recipes.models import Subscribe


class CustomUserViewSet(UserViewSet):
    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.current_user
        return super().get_permissions()
    
#    @action(detail=False, url_path='wtf')
#    def my_subscriptions(self, request):
#        authors = request.user.subscribed_to.all()
#        serializer = CustomUserSubscribeSerializer(authors, many=True)
#        return Response(serializer.data)
