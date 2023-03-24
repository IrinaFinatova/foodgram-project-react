from rest_framework.generics import RetrieveAPIView
from .models import CustomUser
from .serializers import CustomUserSerializer


class UserDetailViewSet(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

