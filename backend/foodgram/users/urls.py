from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
