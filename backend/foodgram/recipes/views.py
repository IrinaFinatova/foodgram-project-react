from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework import filters
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


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context





class CreateDestroyViewSet(CreateModelMixin, DestroyModelMixin,
                                   viewsets.GenericViewSet):
    pass


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    permission_classes = [AllowAny]
    serializer_class = FavoriteSerializer
    http_method_names = ['post', 'delete', 'put', 'delete']

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe,
                                   id=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_destroy(self, instance):
        recipe = get_object_or_404(Recipe,
                                   id=self.kwargs.get('recipe_id'))
        try:
            Favorite.objects.filter(recipe=recipe,
                                    user=self.request.user).delete
        except Http404:
            pass
        return Response(status=HTTP_204_NO_CONTENT)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CartSerializer
    
    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe,
                                   id=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_destroy(self, instance):
        recipe = get_object_or_404(Recipe,
                                   id=self.kwargs.get('recipe_id'))
        try:
            instance.delete(recipe=recipe, user=self.request.user, save=True)
        except Http404:
            pass
        return Response(status=HTTP_204_NO_CONTENT)


class SubscribeListViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeReadSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = Subscribe.objects.filter(subscribed=self.kwargs.get('user_id')).user
        return user
    ## """Метод обработки запроса."""

        #user = get_object_or_404(CustomUser, id=self.kwargs.get('user_id'))
        #return self.request.user.subscribed.all()
        #return Subscribe.objects.filter(user=self.request.user)
        #user_id = self.kwargs.get("user_id")
        #return self.request.user.user.all()
