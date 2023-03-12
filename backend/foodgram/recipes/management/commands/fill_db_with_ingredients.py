import csv
import os

from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient


def create_ingredient(income):
    """Creates Ingredient objects, where "income" is a row in .csv file"""
    Ingredient.objects.get_or_create(name=income[0],
                                     measurement_unit=income[1])


class Command(BaseCommand):
    """Reading the .csv file and filling the database"""
    def handle(self, *args, **options):
        path = os.path.join(BASE_DIR, 'ingredients.csv')
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for ingredient in reader:
                create_ingredient(ingredient)
        self.stdout.write('Database is filled with ingredients!')
