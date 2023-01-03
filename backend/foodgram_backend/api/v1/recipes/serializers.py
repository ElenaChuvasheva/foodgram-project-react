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
    id = SerializerMethodField()
    measurement_unit = SerializerMethodField()
    # чей id нужен?
    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount', 'name', 'measurement_unit')
    
    def get_id(self, obj):
        return obj.ingredient.pk
    
    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit.name


class IngredientAmountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientAmountGetSerializer(many=True, source='ingredientamount_set.all')

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'text', 'cooking_time')


class IngredientsField(serializers.RelatedField):
    def to_representation(self, value):
        print(value)
        serializer = IngredientTypeSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        return data


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsField(queryset=IngredientAmount.objects.all(), many=True)
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients', 'text', 'cooking_time', 'tags')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        author = self.context['request'].user
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            IngredientAmount.objects.create(recipe=recipe, amount=int(ingredient['amount']),
                ingredient=IngredientType.objects.get(pk=int(ingredient['id'])))
        return recipe

    def update(self, instance, validated_data):
        new_tags = validated_data.pop('tags', None)
        if new_tags is not None:
            instance.tags.clear()
            instance.tags.add(*new_tags)

        new_ingredients = validated_data.pop('ingredients', None)
        if new_ingredients is not None:
            instance.ingredients.clear()
            for ingredient in new_ingredients:
                IngredientAmount.objects.create(
                    recipe=instance,
                    ingredient=IngredientType.objects.get(pk=ingredient['id']),
                    amount=ingredient['amount'])
        for attr in validated_data:
            setattr(instance, attr, validated_data[attr])
        instance.save()

        return instance