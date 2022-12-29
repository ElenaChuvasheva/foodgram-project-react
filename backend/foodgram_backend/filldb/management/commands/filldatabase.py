import csv
import logging
import os
import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipes.models import (IngredientAmount, IngredientType, Measure, Recipe,
                            Subscribe, Tag)
from utils.strings import clean_word

User = get_user_model()

CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(settings.BASE_DIR)),
                       'data')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    stream=sys.stdout,
)

INGREDIENTS = 'ingredients'
RECIPES = 'recipes'
INGREDIENTS_AMOUNTS = 'ingredients_amounts'
TAGS = 'tags'
TAGS_RECIPES = 'tags_recipes'
USERS = 'users'
SUBSCRIBES = 'subscribes'


def read_file(filename):
    full_filename = filename + '.csv'
    filepath = os.path.join(CSV_DIR, full_filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
    return reader


def create_objects(row, filename):
    if filename == USERS:
        User.objects.create(
            pk=int(row[0]), username=row[1], email=row[2], role=row[3]
        )
    elif filename == SUBSCRIBES:
        Subscribe.objects.create(
            user=User.objects.get(pk=int(row[0])),
            author=User.objects.get(pk=int(row[1]))
        )
    elif filename == INGREDIENTS:
        name = clean_word(row[0])
        measurement_unit, _ = Measure.objects.get_or_create(name=clean_word(row[1]))
        kwargs = {'name': name,
                  'measurement_unit': measurement_unit}
        IngredientType.objects.create(**kwargs)
    elif filename == RECIPES:
        Recipe.objects.create(pk=int(row[0]),
                              author=User.objects.get(pk=int(row[1])),
                              name=row[2],
                              text=row[3],
                              cooking_time=int(row[4]))
    elif filename == INGREDIENTS_AMOUNTS:
        ingredient = IngredientType.objects.get(pk=int(row[0]))
        recipe = Recipe.objects.get(pk=int(row[2]))
        IngredientAmount.objects.create(ingredient=ingredient,
                                        amount=int(row[1]),
                                        recipe=recipe)
    elif filename == TAGS:
        Tag.objects.create(pk=int(row[0]), name=row[1], slug=row[2], color=row[3])
    elif filename == TAGS_RECIPES:
        tag = Tag.objects.get(pk=int(row[0]))
        recipe = Recipe.objects.get(pk=int(row[1]))
        recipe.tags.add(tag)


def read_to_DB(filename):
    reader = read_file(filename)
    for row in reader:
        create_objects(row, filename)


class Command(BaseCommand):
    help = 'Заполняет базу данных для тестирования'

    def handle(self, *args, **kwargs):
        read_to_DB(USERS)
        read_to_DB(SUBSCRIBES)
        read_to_DB(RECIPES)
        read_to_DB(INGREDIENTS)
        read_to_DB(INGREDIENTS_AMOUNTS)
        read_to_DB(TAGS)
        read_to_DB(TAGS_RECIPES)
        logging.info('база данных готова')
