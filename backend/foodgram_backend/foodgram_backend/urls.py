from http import HTTPStatus

from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import include, path

from recipes.models import IngredientType


def get_file(request):
    if not request.user.is_anonymous:
        recipes = request.user.cart.all()
        ingredients = IngredientType.objects.filter(
            ingredient_amounts__recipe__in=recipes).annotate(
                sum=Sum('ingredient_amounts__amount'))
        text = '\n'.join([f'{p.name}, {p.sum}' for p in ingredients])
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=test.txt'
    else:
        response = HttpResponse('Залогинься', status=HTTPStatus.UNAUTHORIZED)
    return response


urlpatterns = [
    path('for_staff_only/', admin.site.urls),
    path('file/', get_file),
    path('api/', include('api.urls', namespace='api')),
]
