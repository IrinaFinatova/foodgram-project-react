from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import status
from rest_framework.views import APIView

from .models import CustomUser, Subscribe
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from recipes.serializers import SubscribeReadSerializer


class UserDetailViewSet(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=True, methods=['POST', 'DELETE'],
            url_path='(?P<user_id>\d+)/subscribe/',
        url_name='subscribe', permission_classes=(AllowAny,))
    def subscribe(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=self.kwargs.get('user_id'))
        subscribed = get_object_or_404(CustomUser, id=self.request.user.pk)
        if user.pk == subscribed.pk:
            return Response(
                {'error': 'Нельзя подписаться на себя!'},
                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'PUT':
            if Subscribe.objects.filter(
                    user=user, subscribed=subscribed).exist():
                return Response(
                    {'error': 'Вы уже подписаны!'},
                    status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=user, subscribed=subscribed)
        else:
            Subscribe.objects.filter(user=user, subscribed=subscribed).delete()

    @action(detail=True, methods=['get'],
            url_name='listsubscribe', permission_classes=(AllowAny,))
    def subscription(self, request, *args, **kwargs):
        subscribed = get_object_or_404(CustomUser, id=self.request.user.pk)
        user = CustomUser.objects.filter(subscribed=subscribed)
        serializer = SubscribeReadSerializer(user, many=True)
        return Response(serializer.data)
