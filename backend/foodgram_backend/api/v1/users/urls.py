from django.http import HttpResponse
from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import permissions, routers

from api.v1.users.views import CustomUserViewSet

users_list = CustomUserViewSet.as_view(
    {'post': 'create', 'get': 'list'})
users_detail = CustomUserViewSet.as_view(
    {'get': 'retrieve'})
users_subscriptions = CustomUserViewSet.as_view(
    {'get': 'my_subscriptions'})
# пермишен для примера
users_subscribe = CustomUserViewSet.as_view(
    {'post': 'subscribe', 'delete': 'unsubscribe'},
    permission_classes=[permissions.IsAuthenticated])
users_me = CustomUserViewSet.as_view(
    {'get': 'me'})
users_set_password = CustomUserViewSet.as_view(
    {'post': 'set_password'})
users_reset_password = CustomUserViewSet.as_view(
    {'post': 'reset_password'})
users_reset_password_confirm = CustomUserViewSet.as_view(
    {'post': 'reset_password_confirm'})

users_urls = [
    path('', users_list),
    path('<int:id>/', users_detail),
    path('subscriptions/', users_subscriptions),
    path('<int:id>/subscribe/', users_subscribe),
    path('me/', users_me),
    path('set_password/', users_set_password),
    path('reset_password/', users_reset_password),
    path('reset_password_confirm/', users_reset_password_confirm),
]

token_login = TokenCreateView.as_view()
token_logout = TokenDestroyView.as_view()

authtoken_urls = [
    path('login/', token_login),
    path('logout/', token_logout)
]

urlpatterns = [
    path('users/', include(users_urls)),
    # переопределить TokenCreateView из-за кода ответа?
    # ловить response и возвращать с другим кодом?
    path('auth/token/', include(authtoken_urls)),
]
