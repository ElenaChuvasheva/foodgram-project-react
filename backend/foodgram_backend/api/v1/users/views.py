from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response


class CustomUserViewSet(UserViewSet):
    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.current_user
        return super().get_permissions()
