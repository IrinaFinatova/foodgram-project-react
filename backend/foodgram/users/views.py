from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.serializers import SubscribeReadSerializer, SubscribeSerializer

from .models import CustomUser as User
from .models import Subscribe
from .serializers import CustomUserSerializer


class UserDetail(UserViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        data = {'user': id,
                'subscribed': request.user.id}
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Subscribe.objects.filter(**data).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        users = User.objects.filter(
            subscrib__subscribed=self.request.user)
        serializer = SubscribeReadSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
