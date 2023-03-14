from django.contrib import admin
from django.urls import include, path

from api.views import RecipeViewSet


urlpatterns = [
    path('', RecipeViewSet.as_view({'get': 'list'})),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('users.urls')),
]
