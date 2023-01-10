from rest_framework.filters import SearchFilter


class IngredientTypeFilter(SearchFilter):
    search_param = 'name'
