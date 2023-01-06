from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('for_staff_only/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]
