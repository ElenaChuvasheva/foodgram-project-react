from django.contrib import admin

from recipes.models import Subscribe
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name',
                    'last_name', 'role', 'get_subscribers')
    list_editable = ('role',)
    ordering = ('-pk',)

    def get_subscribers(self, obj):
        subscribers = Subscribe.objects.filter(author=obj)
        return '; '.join([p.user.username for p in subscribers])


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_select_related = ('user', 'author')
