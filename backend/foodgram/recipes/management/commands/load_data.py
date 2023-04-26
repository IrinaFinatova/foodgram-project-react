import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


DATA = {
    Ingredient: 'static/data/ingredients.csv'
}


class Command(BaseCommand):
    """Команда для загрузки данных из csv файлов"""

    help = "load data from csv"

    def handle(self, *args, **options):
        for model, file in DATA.items():
            with open(file, "r", encoding="utf-8-sig") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=",")
                for row in csv_reader:
                    try:
                        model.objects.get_or_create(**row)
                        print(f"{file}: {row}")
                    except Exception as error:
                        print(f"Error {error} in file {file}, row{row}")
