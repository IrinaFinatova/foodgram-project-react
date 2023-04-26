from django_filters import FilterSet, ModelMultipleChoiceFilter, NumberFilter

from .models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Фильтр по recipe-фильтрация по автору, тегам, в избранном, в корзинке"""
    author = NumberFilter(field_name='author__id')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all())

    is_favorited = NumberFilter(
        method='get_is_favorited',
        label='В избранном')

    is_in_shopping_cart = NumberFilter(
        method='get_is_in_shopping_cart')

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
