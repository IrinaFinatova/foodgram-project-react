from django.contrib import admin

from .models import (Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag,
                     TagRecipe)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    search_fields = ['name']
    help_search_text = 'Поиск по названию ингредиента'


class IngredientInline(admin.StackedInline):
    model = IngredientRecipe
    extra = 2
    min_num = 1


class TagInline(admin.StackedInline):
    model = TagRecipe
    extra = 2
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [TagInline, IngredientInline]
    list_filter = ('tags', 'name', 'author')
    list_display = ['id', 'author',
                    'name', 'show_tags',
                    'show_ingredients', 'show_favorite']
    search_fields = ('author__last_name',
                     'author__email', 'name')
    help_search_fields = ('Поиск по фамилии или почте '
                          'автора, названию рецепта.')
    date_hierarchy = 'created'

    def show_ingredients(self, obj):
        ingredients_list = []
        for ingredient in obj.ingredients.all():
            ingredients_list.append(ingredient.name.lower())
        return ', '.join(ingredients_list)
    show_ingredients.short_description = 'Ингредиенты'

    def show_tags(self, obj):
        tags_list = []
        for tag in obj.tags.all():
            tags_list.append(tag.name.lower())
        return ', '.join(tags_list)
    show_tags.short_description = 'Теги'

    def show_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    show_favorite.short_description = 'В избранном'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
