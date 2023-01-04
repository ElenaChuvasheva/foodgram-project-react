from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework.generics import ListAPIView

from users.models import Subscribe


class CustomUserViewSet(UserViewSet):
    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.current_user
        return super().get_permissions()


class SubscribeView(ListAPIView):
    def get_queryset(self):
        current_user = self.request.user
        return current_user.subscribed_to.all()
    
#    @action(detail=False, url_path='wtf')
#    def my_subscriptions(self, request):
#        authors = request.user.subscribed_to.all()
#        serializer = CustomUserSubscribeSerializer(authors, many=True)
#        return Response(serializer.data)
