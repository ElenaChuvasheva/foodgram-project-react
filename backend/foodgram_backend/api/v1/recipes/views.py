from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.recipes.serializers import (IngredientTypeSerializer,
                                        RecipeSerializer,
                                        RecipeShortSerializer, TagSerializer)
from api.v1.users.serializers import CustomUserSerializer
from recipes.models import IngredientType, Recipe, Subscribe, Tag
from utils.calculations import is_subscribed

User = get_user_model()

messages = {'unauthorized': 'Пользователь не авторизован',
            'favorite_success': 'Рецепт успешно добавлен в избранное',
            'favorite_fail': 'Ошибка добавления в избранное',
            'unfavorite_fail': 'Ошибка удаления из избранного',
            'cant_subscribe_yourself': 'Нельзя подписаться на себя',
            'subscribed_already': 'Вы уже подписаны на этого пользователя',
            'subscribe_success': 'Подписка успешно создана',
            'no_subscribe': 'Вы не подписаны на этого пользователя',
            'cant_unsubscribe_yourself': 'Нельзя отписаться от себя',
            'unsubscribe_success': 'Вы отписались от этого пользователя'}


# пагинация нужна в итоге?
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientTypeSerializer
    queryset = IngredientType.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    @action(detail=True, url_path='favorite',
            methods=['POST', 'DELETE'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        current_user = request.user
        if request.method == 'POST':
            if not current_user.favorited.filter(pk=pk).exists():
                current_user.favorited.add(recipe)
                serializer = RecipeShortSerializer(recipe)
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response({'errors': messages['favorite_fail']}, status.HTTP_400_BAD_REQUEST)
        if current_user.favorited.filter(pk=pk).exists():
            current_user.favorited.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': messages['unfavorite_fail']}, status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(subscribers__user=current_user)

    @action(detail=True)
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        current_user = self.request.user
        if current_user == author:
            return Response(
                messages['cant_subscribe_yourself'],
                status=status.HTTP_400_BAD_REQUEST)
        if is_subscribed(current_user, author):
            return Response(
                messages['subscribed_already'],
                status=status.HTTP_400_BAD_REQUEST)
        Subscribe.objects.create(user=current_user, author=author)
        return Response(messages['subscribe_success'],
                        status=status.HTTP_201_CREATED)

    @action(detail=True)
    def unsubscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        current_user = self.request.user
        if current_user == author:
            return Response(
                messages['cant_unsubscribe_yourself'],
                status=status.HTTP_400_BAD_REQUEST)
        if not is_subscribed(current_user, author):
            return Response(
                messages['no_subscribe'],
                status=status.HTTP_400_BAD_REQUEST)
        Subscribe.objects.filter(user=current_user, author=author).delete()
        return Response(messages['unsubscribe_success'],
                        status=status.HTTP_204_NO_CONTENT)
