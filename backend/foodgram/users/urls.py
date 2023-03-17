from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path("", include(v1_router.urls)),
    #path("auth/", include(token)),
]