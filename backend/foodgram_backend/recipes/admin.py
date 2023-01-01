from django.contrib import admin

from recipes.models import (IngredientAmount, IngredientType, Measure, Recipe,
                            Subscribe, Tag)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    list_select_related = ('ingredient',)
    raw_id_fields = ('ingredient',)
    verbose_name_plural = 'Ингредиенты'


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'get_tags')
    list_select_related = ('author',)
    list_filter = ('name', 'tags', 'author')
    readonly_fields = ('get_favorited',)
    empty_value_display = '-пусто-'

    def get_tags(self, obj):
        return '; '.join([p.__str__() for p in obj.tags.all()])

    def get_favorited(self, obj):
        return obj.favorited_by.count()

    get_favorited.short_description = 'В избранном, раз'
    get_tags.short_description = 'ТЕГИ'

    inlines = (IngredientAmountInline,)


@admin.register(IngredientType)
class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_select_related = ('measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'amount')
    list_select_related = ('ingredient',)
    search_fields = ('ingredient__name',)
    list_filter = ('ingredient__name',)
    raw_id_fields = ('ingredient',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('pk', 'name', 'slug', 'color')
    empty_value_display = '-пусто-'
