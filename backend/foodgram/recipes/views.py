from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .filters import RecipeFilter
from rest_framework import filters
from rest_framework.decorators import action
from .models import Tag, Ingredient, Recipe, Cart, Favorite
from users.models import Subscribe, CustomUser
from .serializers import (TagSerializer,
                          IngredientSerializer,
                          RecipeReadSerializer,
                          RecipeCreateSerializer,
                          CartSerializer,
                          FavoriteSerializer,
                          SubscribeReadSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = (filters.SearchFilter,)
    search_fields = {'name': ['istartswith', 'icontains']}
    pagination_class = None



class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete']
    #filter_backends = [DjangoFilterBackend]
    #filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

#    def get_serializer_context(self):
#        context = super().get_serializer_context()
#        context.update({'request': self.request})
#        return context

    @action(detail=True, methods=['POST', 'DELETE'],
             permission_classes=(AllowAny,))
    def shopping_cart(self, request, pk):
        data = {'recipe': pk,
                'user': request.user.id}
        if request.method == 'POST':
            serializer = CartSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        Cart.objects.filter(**data).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'], permission_classes=(AllowAny,))
    def favorite(self, request, pk):
        data = {'recipe': pk,
                'user': request.user.id}
        if request.method == 'POST':
            serializer = FavoriteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.filter(**data).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





