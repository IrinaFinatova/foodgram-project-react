from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import CustomUser as User
from users.models import Subscribe
from users.serializers import CustomUserSerializer

from .models import (PARAMETRS_OF_RECIPE, Cart, Favorite, Ingredient,
                     IngredientRecipe, Recipe, Tag, TagRecipe)


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для просмотре тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('__all__',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов для создания рецепта"""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов в рецепте"""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'measurement_unit', 'name', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецепта"""

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
    """Сериализатор для создания рецепта"""

    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    ingredients = IngredientRecipeCreateSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('author', 'tags',
                  'ingredients', 'name',
                  'text', 'image', 'cooking_time')

    def validate(self, data):
        if not data['ingredients']:
            raise serializers.ValidationError('Из чего готовить будем?')
        for ingredient in data['ingredients']:
            if ingredient['amount'] < PARAMETRS_OF_RECIPE['MIN_AMOUNT_INGRED']:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть равным 0!')
            if ingredient['amount'] > PARAMETRS_OF_RECIPE['MAX_AMOUNT_INGRED']:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть больше 2000!')
        if data['cooking_time'] < PARAMETRS_OF_RECIPE['MIN_COOKING_TIME']:
            raise serializers.ValidationError(
                'Время приготовления не может быть равным 0!')
        if data['cooking_time'] > PARAMETRS_OF_RECIPE['MAX_COOKING_TIME']:
            raise serializers.ValidationError(
                'Время приготовления не может быть больше 500!')
        if not data['tags']:
            raise serializers.ValidationError('Выберите теги!')
        return data

    def create_ingredients(self, recipe, ingredients):
        ingredients_recipe = [
            IngredientRecipe(recipe=recipe,
                             ingredient_id=ingredient['id'],
                             amount=ingredient['amount'])
            for ingredient in ingredients]
        IngredientRecipe.objects.bulk_create(
            ingredients_recipe)

    def create_tags(self, recipe, tags):
        tags_recipe = [
            TagRecipe(recipe=recipe, tag=tag) for tag in tags]
        TagRecipe.objects.bulk_create(tags_recipe)

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(recipe, ingredients)
        self.create_tags(recipe, tags)
        return recipe

    def update(self, instance, validated_data):
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.create_ingredients(instance, ingredients)
        self.create_tags(instance, tags)
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        if validated_data.get('image'):
            instance.image = validated_data.get('image')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context={
            'request': self.context.get('request')}).data


class RecipeSimpleSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта в избранном и корзине"""

    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'text',
                  'cooking_time',)


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания избранного"""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Вы уже подписаны на этот рецепт!'
            )
        ]

    def to_representation(self, instance):
        return RecipeSimpleSerializer(instance.recipe, context={
            'request': self.context.get('request')
        }).data


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для создания корзины"""

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


class SubscribeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения подписок"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User

        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            subscribed=request.user, user=obj).exists()

    def get_recipes(self, author):
        request = self.context.get('request')
        recipes = author.recipes.all()
        return RecipeSimpleSerializer(recipes, many=True,
                                      context={'request': request}).data

    def get_recipes_count(self, author):
        return author.recipes.count()


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания подписок"""

    class Meta:
        model = Subscribe
        fields = ('subscribed', 'user')
        validators = [UniqueTogetherValidator(queryset=Subscribe.objects.all(),
                                              fields=('user', 'subscribed'),
                                              message='Вы уже подписаны!')]

    def validate(self, data):
        if self.context.get('request').user == data['user']:
            raise serializers.ValidationError(
                'На себя нельзя подписываться!')
        return data

    def to_representation(self, instance):
        return SubscribeReadSerializer(
            instance.user,
            context={'request': self.context.get('request')}).data
