# Generated by Django 3.2 on 2023-04-27 21:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_add_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['id'], 'verbose_name': 'Ингрeдиент', 'verbose_name_plural': 'Ингрeдиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-created'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['id'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество должно быть больше 0!'), django.core.validators.MaxValueValidator(2000, message='Количество должно быть не больше 2000!')], verbose_name='Количество ингредиентов'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовления должно быть больше 0!'), django.core.validators.MaxValueValidator(500, message='Время приготовления не должно быть больше 500!')], verbose_name='Время приготовления'),
        ),
    ]
