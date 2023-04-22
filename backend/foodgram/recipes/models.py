from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    validate_image_file_extension,
                                    validate_slug)
from django.db import models

from users.models import CustomUser


PARAMETRS_OF_RECIPE = {'MIN_COOKING_TIME': 1,
                       'MAX_COOKING_TIME': 500,
                       'MIN_AMOUNT_INGRED': 1,
                       'MAX_AMOUNT_INGRED': 2000}


class Ingredient(models.Model):
    """Класс моделей ингредиентов"""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название ингредиента',
        error_messages={'unique': 'Такой ингредиент уже существует!'})
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения ингредиента')

    class Meta:
        verbose_name = 'Ингрeдиент'
        verbose_name_plural = 'Ингрeдиенты'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    """Класс моделей тэгов"""
    name = models.CharField(max_length=256,
                            unique=True,
                            verbose_name='Имя тега')
    color = models.CharField(max_length=7,
                             verbose_name='Цвет тега')
    slug = models.SlugField(unique=True,
                            validators=[validate_slug],
                            max_length=50,
                            error_messages={
                                'unique':
                                    'Тег с таким слагом уже существует!'},
                            verbose_name='Слаг тега')
    constraints = [
        models.UniqueConstraint(
            fields=['name', 'slug'], name='unique_name_slug'
        )
    ]

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс моделей рецептов"""
    author = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Ингрeдиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through="TagRecipe",
        related_name='recipes',
        verbose_name='Tег',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название')
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        default=None,
        verbose_name='Картинка',
        validators=[validate_image_file_extension]
    )

    text = models.TextField(
        verbose_name='Описание')

    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(PARAMETRS_OF_RECIPE['MIN_COOKING_TIME'],
                              message=(
                                  'Время приготовления'
                                  ' должно быть больше 0!')),
            MaxValueValidator(PARAMETRS_OF_RECIPE['MAX_COOKING_TIME'],
                              message=('Время приготовления '
                                       'не должно быть больше 500!'))],
        verbose_name='Время приготовления')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created']

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Таблица для ManyToMany связи между Ингридиентами и Рецептами"""

    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   verbose_name='Ингредиенты рецепта')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(PARAMETRS_OF_RECIPE['MIN_AMOUNT_INGRED'],
                              message=(
                                  'Количество должно быть больше 0!')),
            MaxValueValidator(PARAMETRS_OF_RECIPE['MAX_AMOUNT_INGRED'],
                              message=(
                                  'Количество должно быть не больше 2000!'))
        ],
        verbose_name='Количество ингредиентов')

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        ordering = ['ingredient', 'amount']

    def __str__(self):
        return f'{self.recipe.name} {self.ingredient.name}'


class TagRecipe(models.Model):
    """Таблица для ManyToMany связи между Тэгом и Рецептами"""

    tag = models.ForeignKey(Tag,
                            on_delete=models.SET_NULL,
                            null=True,
                            verbose_name='Теги рецепта')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'
        ordering = ['recipe']

    def __str__(self):
        return f'{self.recipe.name} {self.tag.name}'


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='favorite',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorite',
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ('user', )
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_favorite')]

    def __str__(self):
        return f'{self.user.last_name} {self.recipe.name}'


class Cart(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='cart',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='cart',
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Рецепт в корзинке'
        verbose_name_plural = 'Рецепты в корзинке'
        ordering = ('user', )
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_cart')]

    def __str__(self):
        return f'{self.user.last_name} {self.recipe.name}'
