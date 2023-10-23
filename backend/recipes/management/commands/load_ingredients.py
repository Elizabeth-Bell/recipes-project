import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient

PATH = {Ingredient: 'data/ingredients.csv'}


def ingredients_import():
    """Функция распаковки и создания объектов модели Ингредиенты."""
    for model, path in PATH.items():
        with open(path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for name, unit in csv_reader:
                print(name, unit)
                model.objects.create(name=name,
                                     measurement_unit=unit)


class Command(BaseCommand):
    """Создание команды для выполнения импорта csv-файла."""
    def handle(self, *args, **options):
        ingredients = Ingredient.objects.all()
        ingredients.delete()
        ingredients_import()
        self.stdout.write(self.style.SUCCESS('Ингредиенты загружены'))
