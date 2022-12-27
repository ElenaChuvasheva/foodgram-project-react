from django.core.validators import (MaxLengthValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class Measure(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=200,
        unique=True,
        validators=[
            MaxLengthValidator(
                limit_value=200, message='Длина названия не более 200 знаков'
            )]
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientType(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=200,
        db_index=True,
        validators=[
            MaxLengthValidator(
                limit_value=200, message='Длина названия не более 200 знаков'
            )]
    )
    measurement_unit = models.ForeignKey(
        Measure,
        on_delete=models.PROTECT,
        related_name='ingredients',
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Вид ингредиента'
        verbose_name_plural = 'Виды ингредиентов'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(fields=('name', 'measurement_unit'),
                                    name='unique_name_measurement_unit'),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
        unique=True,
        validators=[
            MaxLengthValidator(
                limit_value=200, message='Длина названия не более 200 знаков'
            )]
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug',
        max_length=200,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$', message='Используйте латинские буквы, цифры, знаки _, -'
            ),
            MaxLengthValidator(
                limit_value=200, message='Длина названия не более 200 знаков'
            )]
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=7,
        validators=[
            MaxLengthValidator(
                limit_value=7, message='Длина строки не более 7 знаков'
            )]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('pk',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        validators=[
            MaxLengthValidator(
                limit_value=200, message='Длина названия не более 200 знаков'
            )]
    )
    text = models.TextField(verbose_name='Описание рецепта')
    ingredient_type = models.ManyToManyField(
        IngredientType,
        verbose_name='Вид ингредиента',
        related_name='recipe_ingredient_type',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                limit_value=1, message='Время не может быть меньше 1'
            )]
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipe_tag',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('pk',)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        IngredientType,
        on_delete=models.PROTECT,
        related_name='ingredient_amounts',
        verbose_name='Вид ингредиента'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                limit_value=1, message='Количество не может быть меньше 1'
            )]
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент рецепта'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ('pk',)
        constraints = (
            models.UniqueConstraint(fields=('ingredient', 'recipe'),
                                    name='unique_ingredient_recipe'),
        )

    def __str__(self):
        return f'{self.ingredient.name}, {self.amount} {self.ingredient.measurement_unit}'


# доделать на случай замены ингредиента через админку
@receiver(pre_save, sender=IngredientAmount)
def add_ingredient_saved(sender, instance, **kwargs):
    ingredients_of_recipe = instance.recipe.ingredient_type.all()
    if instance.ingredient not in ingredients_of_recipe:
        instance.recipe.ingredient_type.add(instance.ingredient)
    old_object_qset = IngredientAmount.objects.filter(pk=instance.pk).select_related('ingredient')
    if old_object_qset.exists() and old_object_qset[0].ingredient != instance.ingredient:
        instance.recipe.ingredient_type.remove(old_object_qset[0].ingredient)
        # IngredientType.objects.create(name='smth', measurement_unit=Measure.objects.get(pk=1))


@receiver(pre_delete, sender=IngredientAmount)
def remove_ingredient_deleted(sender, instance, **kwargs):
    instance.recipe.ingredient_type.remove(instance.ingredient)
