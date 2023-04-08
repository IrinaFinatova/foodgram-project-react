from rest_framework.routers import DefaultRouter

from .views import UserDetailViewSet, SubscribeListViewSet, SubscribeDetailViewSet
from django.urls import include, path

router = DefaultRouter()
router.register(
    r'^users/(?P<user_id>\d+)/subscribe', SubscribeDetailViewSet, basename="subscribes")
urlpatterns = [
    path('users/<int:pk>/', UserDetailViewSet.as_view()),
    path(r'users/subscriptions/', SubscribeListViewSet.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
