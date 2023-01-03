from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.recipes.serializers import (IngredientAmountGetSerializer,
                                        IngredientAmountSerializer,
                                        IngredientTypeSerializer,
                                        RecipeGetSerializer, RecipeSerializer,
                                        RecipeShortSerializer, TagSerializer)
from recipes.models import IngredientAmount, IngredientType, Recipe, Tag

messages = {'unauthorized': 'Пользователь не авторизован',
            'favorite_success': 'Рецепт успешно добавлен в избранное',
            'favorite_fail': 'Ошибка добавления в избранное',
            'unfavorite_fail': 'Ошибка удаления из избранного',}


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

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer
        return RecipeSerializer

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
