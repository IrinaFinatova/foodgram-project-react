from django.urls import include, path

from .views import SubscribeViewList, UserDetail, subscribe

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('users/subscription/', SubscribeViewList.as_view()),
    path('users/<int:pk>/subscribe/', subscribe),
    path(r'users/<int:pk>/', UserDetail.as_view())
]
