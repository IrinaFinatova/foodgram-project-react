from .views import UserDetailViewSet
from django.urls import include, path


urlpatterns = [
    path('users/<int:pk>/', UserDetailViewSet.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
