from django.urls import include, path

from api.urls import router_v1
from users.views import UserViewSet

router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]