from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import F, Q

User = get_user_model()


MAX_LENGTH = 200
MAX_LENGTH_COLOR = 7


class Measure(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=MAX_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientType(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=MAX_LENGTH,
        db_index=True,
    )
    measurement_unit = models.ForeignKey(
        Measure,
        on_delete=models.PROTECT,
        related_name='ingredients',
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
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
        max_length=MAX_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug',
        max_length=MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Используйте латинские буквы, цифры, знаки _, -'
            ),
        ]
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=MAX_LENGTH_COLOR,
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
        max_length=MAX_LENGTH,
    )
    text = models.TextField(verbose_name='Описание рецепта')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredient_types = models.ManyToManyField(
        IngredientType,
        verbose_name='Вид ингредиента',
        through='IngredientAmount'
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
        verbose_name='Теги',
    )
    favorited_by = models.ManyToManyField(
        User,
        verbose_name='Избранное',
        related_name='favorited',
        blank=True
    )
    cart_of = models.ManyToManyField(
        User, verbose_name='Корзина',
        related_name='cart',
        blank=True
    )

    image = models.ImageField(
        upload_to='recipes/images/',
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

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
        return (f'{self.ingredient.name}, '
                f'{self.amount} {self.ingredient.measurement_unit}')


class Subscribe(models.Model):
    user = models.ForeignKey(User, related_name='subscribed_to',
                             on_delete=models.CASCADE,
                             verbose_name='Подписчик')
    author = models.ForeignKey(User, related_name='subscribers',
                               on_delete=models.CASCADE,
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(fields=('user', 'author'),
                                    name='unique_user_author'),
            models.CheckConstraint(check=~Q(user=F('author')),
                                   name='author_not_user_constraint')
        )
        ordering = ('author__id',)

    def __str__(self):
        return f'{self.user.username}, {self.author.username}'
