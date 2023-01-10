from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from api.v1.recipes.views import (IngredientTypeViewSet, RecipeViewSet,
                                  SubscriptionViewSet, TagViewSet)
from api.v1.users.views import CustomUserViewSet

app_name = 'api'

users_list = CustomUserViewSet.as_view(
    {'post': 'create', 'get': 'list'})
users_detail = CustomUserViewSet.as_view(
    {'get': 'retrieve'})
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

subscribe_urls = [
    path('subscriptions/', SubscriptionViewSet.as_view(
        {'get': 'list'})),
    path('<int:id>/subscribe/', SubscriptionViewSet.as_view(
        {'post': 'subscribe', 'delete': 'unsubscribe'})),
]

cart_urls = []

v1_recipes_router = routers.DefaultRouter()
v1_recipes_router.register('tags', TagViewSet, basename='tags')
v1_recipes_router.register(
    'ingredients', IngredientTypeViewSet, basename='ingredient_types')
v1_recipes_router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('users/', include(users_urls)),
    path('users/', include(subscribe_urls)),
    path('auth/token/', include(authtoken_urls)),
    path('', include(v1_recipes_router.urls)),
]
