from rest_framework.generics import get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import mixins, viewsets
from .models import CustomUser, Subscribe
from .serializers import CustomUserSerializer


class UserDetailViewSet(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


