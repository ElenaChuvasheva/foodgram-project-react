from django.urls import include, path
from rest_framework import routers

from api.v1.recipes.views import (IngredientTypeViewSet, RecipeViewSet,
                                  TagViewSet)

v1_router = routers.DefaultRouter()
v1_router.register('tags', TagViewSet, basename='tags')
v1_router.register('ingredients', IngredientTypeViewSet, basename='ingredient_types')
v1_router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(v1_router.urls)),
]
