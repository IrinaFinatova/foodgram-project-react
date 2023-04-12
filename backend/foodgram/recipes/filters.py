from django_filters import CharFilter, FilterSet

from .models import Ingredient, Recipe
class IngredientFilter(FilterSet):
    """Фильтры по полям title и text модели Homework"""

    name = CharFilter(field_name='name',
                      lookup_expr=('startswith', 'icontains'),
                       label='Название ингредиента')

    class Meta:
        model = Ingredient
        fields = ('name')