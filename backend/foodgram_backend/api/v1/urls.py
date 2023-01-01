from django.urls import include, path

urlpatterns = [
    path('', include('api.v1.recipes.urls')),
    path('', include('api.v1.users.urls')),
]
