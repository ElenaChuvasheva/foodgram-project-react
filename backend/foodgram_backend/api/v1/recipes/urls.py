from django.urls import include, path
from rest_framework import routers

from api.v1.recipes.views import (IngredientTypeViewSet, RecipeViewSet,
                                  TagViewSet)

v1_recipes_router = routers.DefaultRouter()
v1_recipes_router.register('tags', TagViewSet, basename='tags')
v1_recipes_router.register('ingredients', IngredientTypeViewSet, basename='ingredient_types')
v1_recipes_router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(v1_recipes_router.urls)),
]
