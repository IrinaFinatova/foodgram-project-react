from rest_framework.routers import DefaultRouter

from .views import UserDetailViewSet
from django.urls import include, path

router = DefaultRouter()
#router.register(r'users', UserDetailViewSet, basename="users")
urlpatterns = [
    path(r'users', UserDetailViewSet, basename="users"),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
