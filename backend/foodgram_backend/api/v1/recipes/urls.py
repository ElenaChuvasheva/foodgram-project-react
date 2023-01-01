from django.urls import include, path
from rest_framework import routers

from api.v1.recipes.views import TagViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(v1_router.urls)),
]
