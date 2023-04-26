from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipes.serializers import SubscribeSerializer, SubscribeReadSerializer
from .models import CustomUser, Subscribe
from .serializers import CustomUserSerializer


class UserDetail(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class SubscribeViewList(ListAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeReadSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return CustomUser.objects.filter(
            subscrib__subscribed=self.request.user)


@permission_classes(IsAuthenticated,)
@api_view(['POST', 'DELETE'])
def subscribe(request, pk):
    data = {'user': pk,
            'subscribed': request.user.id}
    if request.method == 'POST':
        serializer = SubscribeSerializer(
            data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    Subscribe.objects.filter(**data).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
