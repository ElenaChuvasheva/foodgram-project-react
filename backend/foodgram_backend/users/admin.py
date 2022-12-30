from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from recipes.models import Recipe, Subscribe
from users.models import CustomUser


class FavoritedInline(admin.TabularInline):
    model = Recipe.favorited_by.through
    verbose_name_plural = 'Избранное'
    verbose_name = 'Рецепт'


class CartInline(admin.TabularInline):
    model = Recipe.cart_of.through
    verbose_name_plural = 'Покупки'
    verbose_name = 'Рецепт'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ('-pk',)

    def get_list_display(self, request):
        result = ['pk', 'email', 'username', 'first_name',
                  'last_name', 'get_subscribers',
                  'get_subscribed_to']
        if request.user.is_superuser:
            result.append('role')
            self.list_editable = ('role',)
        return result

    def get_subscribers(self, obj):
        subscribers = Subscribe.objects.filter(author=obj)
        return '; '.join([p.user.username for p in subscribers])

    def get_subscribed_to(self, obj):
        subscribed_to = Subscribe.objects.filter(user=obj)
        return '; '.join([p.author.username for p in subscribed_to])

    def get_readonly_fields(self, request, obj=None):
        result = []
        if not request.user.is_superuser:
            result.extend(['is_superuser', 'user_permissions', 'groups'])
            if not request.user == obj:
                result.extend(['is_staff', 'first_name', 'last_name', 'email',
                               'username'])
                if obj.is_superuser or obj.is_staff:
                    result.extend(['password', 'is_active'])
        return result

    get_subscribers.short_description = 'Подписчики'
    get_subscribed_to.short_description = 'Авторы'

    inlines = (FavoritedInline, CartInline,)
