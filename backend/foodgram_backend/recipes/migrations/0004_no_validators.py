# Generated by Django 2.2.19 on 2023-01-03 09:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredienttype',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название рецепта'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, verbose_name='Цвет тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(message='Используйте латинские буквы, цифры, знаки _, -', regex='^[-a-zA-Z0-9_]+$')], verbose_name='Slug'),
        ),
    ]
