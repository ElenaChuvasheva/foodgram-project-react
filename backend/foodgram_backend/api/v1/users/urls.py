from django.urls import include, path
from djoser.views import TokenCreateView, UserViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'post': 'create'})),
    # переопределить TokenCreateView из-за кода ответа?
    # ловить response и возвращать с другим кодом?
    path('auth/token/login/', TokenCreateView.as_view()),
#    path('', include('djoser.urls')),
#    path('auth/', include('djoser.urls.jwt')),
#    path('auth/', include('djoser.urls.authtoken'))
]
