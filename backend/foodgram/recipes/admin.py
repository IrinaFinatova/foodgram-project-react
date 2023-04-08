from django.contrib import admin
from .models import Tag, Ingredient, Recipe, IngredientRecipe, TagRecipe, Cart

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']


class IngredientInline(admin.StackedInline):
    model = IngredientRecipe
    extra = 2


class TagInline(admin.StackedInline):
    model = TagRecipe
    extra = 2


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [TagInline, IngredientInline]
    list_display = ['id', 'author', 'name', 'show_tags', 'show_ingredients']

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
    show_ingredients.show_tags = 'Теги'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user']
