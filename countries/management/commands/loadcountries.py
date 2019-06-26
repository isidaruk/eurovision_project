import csv

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from countries.models import Country


class Command(BaseCommand):
    help = 'Loads a data to the Country table in the database from the specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The CSV file to load data from')

    def process_file(self, reader):
        for line in reader:
            country_name = line[0]

            if not country_name:
                self.stdout.write(self.style.WARNING('Data is invalid (empty). Skipped.'))
                continue

            # Check to see if country is already in database.
            if Country.objects.filter(name=country_name).exists():
                self.stdout.write(self.style.WARNING(
                    f"Name: '{country_name}'' is already exists in the Country table in database. Skipped."
                ))
            else:
                c = Country(name=country_name)
                c.save()

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']

        data = None

        try:
            with open(f'{csv_filename}', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                # The first line is the header, loop over the first line.
                next(csv_reader)
                data = list(csv_reader)

        except FileNotFoundError:
            raise CommandError(f"File '{csv_filename}' does not exist.")

        if data:
            self.process_file(data)
            self.stdout.write(self.style.SUCCESS(
                f"Successfully downloaded data to the Country table in database from '{csv_filename}'."
            ))
        else:
            self.stdout.write(self.style.WARNING('The input file is empty.'))
