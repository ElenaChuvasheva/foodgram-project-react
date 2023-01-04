from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from api.v1.users.serializers import CustomUserSerializer
from recipes.models import IngredientAmount, IngredientType, Recipe, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientTypeSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = IngredientType
        fields = '__all__'


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient.pk', queryset=IngredientType.objects.all())
    name = serializers.PrimaryKeyRelatedField(source='ingredient.name', queryset=IngredientType.objects.all(), required=False)
    measurement_unit = serializers.PrimaryKeyRelatedField(source='ingredient.measurement_unit.name', queryset=IngredientType.objects.all(), required=False)
    # чей id нужен?
    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount', 'name', 'measurement_unit')

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError('Количество не может быть меньше 1')
        return value
    

# также к вопросу о выдаче
class TagsField(serializers.RelatedField):
    def to_internal_value(self, data):
        return data
    
    def to_representation(self, value):
        serializer = TagSerializer(value)
        return serializer.data


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(source='ingredientamount_set.all', many=True)
    author = CustomUserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    # убрать tags = ... или сделать через primarykey, если выдача неважна
    tags = TagsField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients', 'text', 'cooking_time',
                  'tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        return self.context['request'].user in obj.favorited_by.all()

    def get_is_in_shopping_cart(self, obj):
        return self.context['request'].user in obj.cart_of.all()

    def validate_ingredients(self, value):
        ingredients_list = [v['ingredient']['pk'] for v in value]
        if len(set(ingredients_list)) != len(ingredients_list):
            raise serializers.ValidationError('Ингредиенты не должны повторяться')
        if not value:
            raise serializers.ValidationError('Список ингредиентов не может быть пустым')
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError('Список тегов не может быть пустым')
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        author = self.context['request'].user
        ingredients = validated_data.pop('ingredientamount_set').pop('all')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.__make_tags(recipe, tags)
        self.__make_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        new_tags = validated_data.pop('tags', None)
        if new_tags is not None:
            instance.tags.clear()
            self.__make_tags(instance, new_tags)
        if 'ingredientamount_set' in validated_data:
            new_ingredients = validated_data.pop('ingredientamount_set', None).pop('all', None)
            instance.ingredient_types.clear()
            self.__make_ingredients(instance, new_ingredients)
        for attr in validated_data:
            setattr(instance, attr, validated_data[attr])
        instance.save()
        return instance

    def __make_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient['ingredient']['pk'],
                amount=ingredient['amount'])

    def __make_tags(self, recipe, tags):
        for tag in tags:
            recipe.tags.add(tag)
