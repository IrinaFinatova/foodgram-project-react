
import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Recipe, Ingredient, Tag, Favorite, Cart, IngredientRecipe, TagRecipe
from users.serializers import CustomUserSerializer




class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('__all__',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()
    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'measurement_unit', 'name', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time',)

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return Favorite.objects.filter(recipe=obj.id, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return Cart.objects.filter(recipe=obj.id, user=user).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientRecipeCreateSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'ingredients', 'name', 'text', 'image', 'cooking_time')

    def validate(self, data):
        if not data['ingredients']:
            raise serializers.ValidationError('Из чего готовить будем?')
        for ingredient in data['ingredients']:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть равным 0!')
        if data['cooking_time'] < 1:
            raise serializers.ValidationError(
                'Время приготовления не может быть равным 0!')
        if not data['tags']:
            raise serializers.ValidationError('Выберите теги!')
        return data

    def create_ingredients_tags(self, recipe, ingredients, tags):
        for ingredient in ingredients:
            IngredientRecipe.objects.create(recipe=recipe,
                                            ingredient=ingredient['id'],
                                            amount=ingredient['amount'])
        for tag in tags:
            TagRecipe.objects.create(recipe=recipe, tag=tag)

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients_tags(recipe, ingredients, tags)
        return recipe

    def update(self, instance, validated_data):
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.create_ingredients_tags(instance, ingredients, tags)
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        if validated_data.get('image'):
            instance.image = validated_data.get('image')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class RecipeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id'
                  'name',
                  'image',
                  'text',
                  'cooking_time',)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=('user', 'recipe'),
                message='Вы уже подписаны на этот рецепт!'
            )
        ]

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=('user', 'recipe'),
                message='Этот рецепт уже есть в корзине!'
            )
        ]

    def to_representation(self, instance):
        return RecipeSimpleSerializer(instance.recipe, context={
            'request': self.context.get('request')}).data
