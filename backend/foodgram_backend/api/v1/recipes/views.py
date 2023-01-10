import operator
from functools import reduce

from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.filters import IngredientTypeFilter
from api.v1.permissions import IsAuthorOrReadOnly
from api.v1.recipes.serializers import (CustomUserSubscribeSerializer,
                                        IngredientTypeSerializer,
                                        RecipeSerializer,
                                        RecipeShortSerializer, TagSerializer)
from recipes.models import IngredientType, Recipe, Subscribe, Tag
from utils.calculations import is_subscribed

User = get_user_model()

messages = {'unauthorized': 'Пользователь не авторизован',
            'favorite_success': 'Рецепт успешно добавлен в избранное',
            'favorite_fail': 'Этот рецепт уже есть в избранном',
            'unfavorite_fail': 'Этого рецепта нет в избранном',
            'cant_subscribe_yourself': 'Нельзя подписаться на себя',
            'subscribed_already': 'Вы уже подписаны на этого пользователя',
            'no_subscribe': 'Вы не подписаны на этого пользователя',
            'cant_unsubscribe_yourself': 'Нельзя отписаться от себя',
            'in_cart_already': 'Этот рецепт уже есть в списке покупок',
            'not_in_cart': 'Этого рецепта нет в списке покупок'}


def get_error_context(message):
    return {'errors': message}


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientTypeViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = IngredientTypeSerializer
    queryset = IngredientType.objects.all()
    filter_backends = (IngredientTypeFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        q_list = []
        tags_list = self.request.query_params.getlist('tags')
        if tags_list:
            q_list.append(Q(tags__slug__in=tags_list))
        author_id = self.request.query_params.get('author')
        if author_id is not None:
            q_list.append(Q(author__pk=int(author_id)))
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart == str(1):
            q_list.append(Q(pk__in=self.request.user.cart.all()))
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited == str(1):
            q_list.append(Q(pk__in=self.request.user.favorited.all()))
        if q_list:
            return Recipe.objects.filter(
                reduce(operator.and_, q_list)).distinct()
        return Recipe.objects.all()

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
            return Response(get_error_context(messages['favorite_fail']),
                            status.HTTP_400_BAD_REQUEST)
        if current_user.favorited.filter(pk=pk).exists():
            current_user.favorited.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(get_error_context(messages['unfavorite_fail']),
                        status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path='download_shopping_cart', methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        recipes = request.user.cart.all()
        ingredients = IngredientType.objects.filter(
            ingredient_amounts__recipe__in=recipes).annotate(
                sum=Sum('ingredient_amounts__amount'))
        text = '\n'.join([f'{p.name}, {p.sum} {p.measurement_unit.name}'
                          for p in ingredients])
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=test.txt'
        return response

    @action(detail=True, url_path='shopping_cart', methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        current_user = request.user
        if request.method == 'POST':
            if not current_user.cart.filter(pk=pk).exists():
                current_user.cart.add(recipe)
                serializer = RecipeShortSerializer(recipe)
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(get_error_context(messages['in_cart_already']),
                            status.HTTP_400_BAD_REQUEST)
        if current_user.cart.filter(pk=pk).exists():
            current_user.cart.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(get_error_context(messages['not_in_cart']),
                        status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CustomUserSubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(subscribers__user=current_user)

    @action(detail=True)
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        current_user = self.request.user
        if current_user == author:
            return Response(
                get_error_context(messages['cant_subscribe_yourself']),
                status=status.HTTP_400_BAD_REQUEST)
        if is_subscribed(current_user, author):
            return Response(
                get_error_context(messages['subscribed_already']),
                status=status.HTTP_400_BAD_REQUEST)
        Subscribe.objects.create(user=current_user, author=author)
        serializer = self.get_serializer(author)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    @action(detail=True)
    def unsubscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        current_user = self.request.user
        if current_user == author:
            return Response(
                get_error_context(messages['cant_unsubscribe_yourself']),
                status=status.HTTP_400_BAD_REQUEST)
        if not is_subscribed(current_user, author):
            return Response(
                get_error_context(messages['no_subscribe']),
                status=status.HTTP_400_BAD_REQUEST)
        Subscribe.objects.filter(user=current_user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
