import csv

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from contests.models import Contest
from countries.models import Country


class Command(BaseCommand):
    help = 'Loads a data to the Contest table in the database from the specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The CSV file to load data from')

    def process_file(self, reader):
        for line in reader:
            year = line[0]
            country = line[1]

            if not (year and country):
                self.stdout.write(self.style.WARNING(f"Data is invalid (or empty: '{year}', '{country}'). Skipped."))
                break

            # Check to see if there is a country in database with the given id.
            if Country.objects.filter(id=country).exists():

                # The year of the Contest should be unique.
                if Contest.objects.filter(year=year).exists():
                    self.stdout.write(self.style.WARNING(
                        f"The Contest with the year {year} exists in database. Skipped."
                    ))
                else:
                    contest = Contest(year=year, host_country=Country.objects.get(id=country))
                    contest.save()
            else:
                self.stdout.write(self.style.WARNING(
                    f"""Country with the given ID: {country} does not exists in database.
                    First run the 'loadcountries' command or create Country with that ID manually. Skipped."""
                ))

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
                f"Successfully downloaded data to the Contest table in database from '{csv_filename}'."
            ))
        else:
            self.stdout.write(self.style.WARNING('The input file is empty.'))
