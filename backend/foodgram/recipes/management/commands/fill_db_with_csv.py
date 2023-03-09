import csv
import os
from os.path import dirname
import sys

from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

PROJECT_DIR = dirname(dirname(BASE_DIR))


def create_ingredient(income):
    """Creates Ingredient objects, where "income" is a row in .csv file"""
    Ingredient.objects.get_or_create(name=income[0],
                                     measurement_unit=income[1])


class Command(BaseCommand):
    """Reading the .csv file and filling the database"""
    help = 'Load ingredients to database'

    def handle(self, *args, **options):
        if sys.platform.lower().startswith('win'):
            path = os.path.join(PROJECT_DIR, 'data\ingredients.csv')
        else:
            path = os.path.join(PROJECT_DIR, 'data/ingredients.csv')
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for ingredient in reader:
                create_ingredient(ingredient)
        self.stdout.write('Database is filled!')
