from django.http import HttpResponse
from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView  # , UserViewSet

from api.v1.users.views import CustomUserViewSet

users_urls = [
    path('', CustomUserViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('<int:id>/', CustomUserViewSet.as_view({'get': 'retrieve'})),
    path('me/', CustomUserViewSet.as_view({'get': 'me'})),
    path('set_password/', CustomUserViewSet.as_view(
        {'post': 'set_password'})
    ),
    path('reset_password/', CustomUserViewSet.as_view(
        {'post': 'reset_password'})),
    path('reset_password_confirm/', CustomUserViewSet.as_view(
        {'post': 'reset_password_confirm'})),
]

authtoken_urls = [
    path('login/', TokenCreateView.as_view()),
    path('logout/', TokenDestroyView.as_view())
]

urlpatterns = [
    path('users/', include(users_urls)),
    # переопределить TokenCreateView из-за кода ответа?
    # ловить response и возвращать с другим кодом?
    path('auth/token/', include(authtoken_urls)),
]
