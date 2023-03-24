import webcolors
import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Recipe, Ingredient, Tag
from users.serializers import UserSerializer
from rest_framework.serializers import (
    CurrentUserDefault,
    SlugRelatedField,
)

class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'title', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'tags', 'name', 'text', 'image', 'cooking_time')
        read_only_fields = ('author',)

class RecipeCreateSerializer(serializers.ModelSerializer):

    ingredients = SlugRelatedField(
        queryset=Ingredient.objects.all(), slug_field="title", many=True
    )
    image = Base64ImageField(required=False, allow_null=True)
    tags = SlugRelatedField(
        queryset=Tag.objects.all(), slug_field='slug', many=True)

    class Meta:
       model = Recipe
       fields = ('name', 'text', 'cooking_time', 'ingredients', 'tags')
