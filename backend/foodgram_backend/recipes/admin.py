from django.contrib import admin
from recipes.models import IngredientAmount, IngredientType, Recipe, Tag


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    raw_id_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_ingredient_types', 'get_tags')
    list_filter = ('name', 'tags')
    fields = ('name', 'text', 'cooking_time', 'tags')
    empty_value_display = '-пусто-'

    def get_ingredient_types(self, obj):
        return '; '.join([p.__str__() for p in obj.ingredient_type.all()])

    def get_tags(self, obj):
        return '; '.join([p.__str__() for p in obj.tags.all()])

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
