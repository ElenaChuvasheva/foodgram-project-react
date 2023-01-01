from rest_framework import viewsets

from api.v1.recipes.serializers import TagSerializer
from recipes.models import Tag


class GetPostPatchDeleteViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
