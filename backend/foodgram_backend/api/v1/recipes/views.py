from rest_framework import filters, viewsets

from api.v1.recipes.serializers import (IngredientAmountGetSerializer,
                                        IngredientAmountSerializer,
                                        IngredientTypeSerializer,
                                        RecipeGetSerializer, RecipeSerializer,
                                        TagSerializer)
from recipes.models import IngredientAmount, IngredientType, Recipe, Tag


class GetPostPatchDeleteViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')


# пагинация нужна в итоге?
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientTypeSerializer
    queryset = IngredientType.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(GetPostPatchDeleteViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer
        return RecipeSerializer
