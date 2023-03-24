from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeCreateSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        """Метод предопределения автора."""
        serializer.save(author=self.request.user)


    def get_serializer_class(self):
        """Метод предопределения сериализатора в зависимости от запроса."""
        if self.action in ("list", "retrieve"):
            return RecipeSerializer
        return RecipeCreateSerializer