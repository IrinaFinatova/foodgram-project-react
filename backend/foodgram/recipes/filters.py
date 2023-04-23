from django_filters import (BooleanFilter, CharFilter, FilterSet,
                            ModelMultipleChoiceFilter)

from .models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Фильтр по recipe-фильтрация по автору, тегам, в избранном, в корзинке"""
    author = CharFilter(label='Автор рецепта')
    tags = ModelMultipleChoiceFilter(
        name='tags__slug', lookup_type='iexact',
        queryset=Tag.objects.all(),
        label='Теги')
    is_favorited = BooleanFilter(
        method='get_is_favorited',
        label='В избранном')
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart',
        label='В корзинке')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, field_name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, field_name, value):
        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset
