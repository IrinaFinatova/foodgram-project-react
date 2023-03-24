from django.db import models
from django.core.validators import validate_slug, validate_image_file_extension
from users.models import CustomUser


class Ingredient(models.Model):
    """Класс моделей ингридиентов"""
    title = models.CharField(
        max_length=250, unique=True, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=250, verbose_name='Единица измерения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Tag(models.Model):
    """Класс моделей тэгов"""
    name = models.CharField(max_length=256,
                            verbose_name='Имя')
    color = models.CharField(max_length=256,
                             verbose_name='Цвет')
    slug = models.SlugField(unique=True,
                            validators=[validate_slug],
                            max_length=50,
                            verbose_name='Слаг')
    constraints = [
        models.UniqueConstraint(
            fields=["name", "slug"], name="unique_name_slug"
        )
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


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
        verbose_name='Ингридиенты',
        db_index=True,)
    tags = models.ManyToManyField(
        Tag,
        through="TagRecipe",
        db_index=True,
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
        verbose_name='Время приготовления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['name']


    def __str__(self):
        return self.name

class IngredientRecipe(models.Model):
    """Таблица для ManyToMany связи между Ингридиентами и Рецептами"""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class TagRecipe(models.Model):
    """Таблица для ManyToMany связи между Тэгом и Рецептами"""

    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
