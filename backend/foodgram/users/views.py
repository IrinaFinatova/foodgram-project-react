from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from .models import CustomUser, Subscribe
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from recipes.serializers import SubscribeSerializer, SubscribeReadSerializer


class UserDetail(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


@api_view(['GET'])
def subscription(request):
    users = CustomUser.objects.filter(subscrib__subscribed=request.user)
    serializer = SubscribeReadSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST', 'DELETE'])
def subscribe(request, pk):
    data = {'user': pk,
            'subscribed': request.user.id}
    if request.method == 'POST':
        serializer = SubscribeSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    Subscribe.objects.filter(**data).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

