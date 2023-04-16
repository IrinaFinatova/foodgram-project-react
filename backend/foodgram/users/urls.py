from rest_framework.routers import DefaultRouter

from .views import UserDetail, subscription, subscribe
from django.urls import include, path


urlpatterns = [
    path('users/subscription/', subscription),
    path('users/<int:pk>/subscribe/', subscribe),
    path(r'users/<int:pk>/', UserDetail.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    ]
