"""foodgram URL Configuration"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'),
    path('api/users/', include('users.urls')),
    #path('api/auth/', include('djoser.urls')),
    #re_path(r'^auth/', include('djoser.urls.authtoken'))
]
