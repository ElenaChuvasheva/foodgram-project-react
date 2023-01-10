from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.views import UserViewSet

from api.v1.pagination import CustomPagination

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.current_user
        return super().get_permissions()
