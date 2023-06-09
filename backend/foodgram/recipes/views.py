from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag
from .permissions import IsOwnerOrIsStaffPermission
from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipeReadSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра ингредиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет на основе модели рецептов для создания,
     удаления, мзменения и просмотра рецепта(рецептов)"""

    queryset = Recipe.objects.all()
    permission_classes = [IsOwnerOrIsStaffPermission]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        """Добавление рецепта в корзину
        для покупки ингрeдиентов"""

        data = {'recipe': pk,
                'user': request.user.id}
        if request.method == 'POST':
            serializer = CartSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        Cart.objects.filter(**data).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        """Добавление рецепта в избранное
         и его удаление из избранного."""

        data = {'recipe': pk,
                'user': request.user.id}
        if request.method == 'POST':
            serializer = FavoriteSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        Favorite.objects.filter(**data).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes(IsAuthenticated,)
@api_view(['GET'])
def download_shopping_cart(request):
    """Скачивание списка  ингридиентов(название и количество)
     в пдф формате"""

    ingredient_list = "Cписок покупок:"
    ingredients = IngredientRecipe.objects.filter(
        recipe__cart__user=request.user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    for num, i in enumerate(ingredients):
        ingredient_list += (
            f"\n{i['ingredient__name']} - "
            f"{i['amount']} {i['ingredient__measurement_unit']}"
        )
        if num < ingredients.count() - 1:
            ingredient_list += ', '
    file = 'shopping_list'
    response = HttpResponse(ingredient_list, 'Content-Type: application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
    return response
