from django.core.management.base import BaseCommand, CommandError
from countries.models import Country

import csv


class Command(BaseCommand):
    help = 'Loads a data to the Country table in the database from the specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The CSV file to load data from')

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']

        try:
            with open(f'{csv_filename}', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                next(csv_reader)  # The first line is the header, loop over the first line.

                for line in csv_reader:
                    country_name = line[0]

                    # Check to see if country is already in database.
                    if Country.objects.filter(name=country_name).exists():
                        self.stdout.write(self.style.WARNING(
                            f"Some data (field Name: {country_name}) is already exists in the Country table in database. Skipped."
                        ))
                    else:
                        c = Country(name=country_name)
                        c.save()

        except Exception as e:
            raise CommandError(f"File '{csv_filename}' does not exist.")

        self.stdout.write(self.style.SUCCESS(
            f"Data was successfully downloaded to the Country table in database from '{csv_filename}'."))
