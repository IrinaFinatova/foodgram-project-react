from rest_framework.generics import get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import mixins, viewsets
from .models import CustomUser, Subscribe
from .serializers import CustomUserSerializer, SubscribeSerializer


class UserDetailViewSet(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class SubscribeListViewSet(ListAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()

    def get_queryset(self):
        """Метод обработки запроса."""

        #user = get_object_or_404(CustomUser, id=self.kwargs.get('user_id'))
        return self.request.user.subscribed.all()
        #return Subscribe.objects.filter(user=self.request.user)
        #user_id = self.kwargs.get("user_id")
        #return self.request.user.user.all()

class CreateRetrieveDestroyViewSet(mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    pass

class SubscribeDetailViewSet(CreateRetrieveDestroyViewSet):
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(CustomUser, id=self.kwargs.get('user_id'))
        serializer.save(followed=self.request.user, user=user)

