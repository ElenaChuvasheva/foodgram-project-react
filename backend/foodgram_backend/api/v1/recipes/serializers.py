from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from api.v1.users.serializers import CustomUserSerializer
from recipes.models import IngredientAmount, IngredientType, Recipe, Tag

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientTypeSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = IngredientType
        fields = '__all__'


class IngredientAmountGetSerializer(serializers.ModelSerializer):
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()
    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount', 'name', 'measurement_unit')
    
    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit.name


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientAmountGetSerializer(many=True, source='ingredientamount_set.all')

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'text', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'text', 'cooking_time', 'author')
