from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserDetail

router_v1 = DefaultRouter()
router_v1.register('', UserDetail, basename='users')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include(router_v1.urls)),
]
