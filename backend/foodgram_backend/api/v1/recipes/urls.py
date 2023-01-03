from django.urls import include, path
from rest_framework import routers

from api.v1.recipes.views import (IngredientTypeViewSet, RecipeViewSet,
                                  TagViewSet)

v1_router = routers.DefaultRouter()
v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'ingredients', IngredientTypeViewSet, basename='ingredient_types')
v1_router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(v1_router.urls)),
]
