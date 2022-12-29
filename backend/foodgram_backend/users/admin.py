from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name',
                    'last_name', 'role', 'get_subscribers',
                    'get_subscribed_to')
    list_editable = ('role',)
    ordering = ('-pk',)

    def get_subscribers(self, obj):
        subscribers = obj.subscribers.all()
        return '; '.join([p.username for p in subscribers])

    def get_subscribed_to(self, obj):
        subscribed_by = obj.subscribed_to.all()
        return '; '.join([p.username for p in subscribed_by])
