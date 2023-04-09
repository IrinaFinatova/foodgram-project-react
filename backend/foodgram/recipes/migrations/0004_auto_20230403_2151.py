# Generated by Django 3.2 on 2023-04-03 18:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230401_2127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'ordering': ['ingredient', 'amount'], 'verbose_name': 'Ингредиенты рецепта', 'verbose_name_plural': 'Ингредиенты рецепта'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['name', 'author'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tagrecipe',
            options={'ordering': ['tag'], 'verbose_name': 'Теги рецепта', 'verbose_name_plural': 'Теги рецепта'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=200, verbose_name='Единица измерения ингредиента'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(error_messages={'unique': 'Такой ингредиент уже существует!'}, max_length=200, unique=True, verbose_name='Название ингредиента'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество должно быть больше 0!')], verbose_name='Количество ингредиентов'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовления должно быть больше 0!')], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(db_index=True, related_name='recipes', through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='Ингрeдиенты'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(error_messages={'unique': 'Тег с таким слагом уже существует!'}, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')], verbose_name='Слаг тега'),
        ),
        migrations.AlterField(
            model_name='tagrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='tagrecipe',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.tag', verbose_name='Теги рецепта'),
        ),
    ]
