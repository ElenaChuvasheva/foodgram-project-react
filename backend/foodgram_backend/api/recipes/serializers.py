# from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Tag


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Tag.objects.all())]
    )
    # валидатор на длину?
    color = serializers.CharField()

    slug = serializers.SlugField(validators=[
        UniqueValidator(queryset=Tag.objects.all())
    ])
#            RegexValidator(
#                regex=r'^[-a-zA-Z0-9_]+$',
#                message='Используйте латинские буквы, цифры, знаки _, -'
#            ),

    class Meta:
        model = Tag
        fields = '__all__'
