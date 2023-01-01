from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import resolve

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


class SubscribeInline(admin.TabularInline):
    model = Subscribe
    fk_name = 'user'
    verbose_name = 'Подписка'
    verbose_name_plural = 'Подписки'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            resolved = resolve(request.path_info)
            kwargs['queryset'] = CustomUser.objects.exclude(pk=resolved.kwargs['object_id'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ('-pk',)

    def get_list_display(self, request):
        result = ['pk', 'email', 'username', 'first_name',
                  'last_name', 'get_subscribers',
                  'get_subscribed_to', 'get_role']
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

    def get_role(self, obj):
        return obj.role

    def get_readonly_fields(self, request, obj=None):
        result = []
        if not request.user.is_superuser:
            result.extend(['is_superuser', 'user_permissions', 'groups', 'is_staff'])
            if obj is not None:
                admin_not_me = obj.is_admin and request.user != obj
                if admin_not_me:
                    result.extend(['password', 'is_active', 'first_name',
                                   'last_name', 'email', 'username'])
        return result

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return False
        return request.user.is_superuser or request.user == obj or request.user.is_admin and not obj.is_admin

    get_subscribers.short_description = 'Подписчики'
    get_subscribed_to.short_description = 'Авторы'

    inlines = (FavoritedInline, CartInline, SubscribeInline)
