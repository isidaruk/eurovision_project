from django.core.management.base import BaseCommand, CommandError
from contests.models import Contest
from countries.models import Country

import csv


class Command(BaseCommand):
    help = 'Imports a data to the Contest table in the database from the specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The CSV file to load data from')

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']

        try:
            with open(f'{csv_filename}.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                next(csv_reader)  # The first linie is the header, loop over the first line.

                for line in csv_reader:
                    year = line[0]
                    country_id = line[1]

                    # Check to see if there is a country in database with the given id.
                    if Country.objects.filter(id=country_id).exists():

                        # The year of the Contest should be unique.
                        if Contest.objects.filter(year=year).exists():
                            self.stdout.write(self.style.WARNING(
                                f"The Contest with the year {year} exists in database. Skipped."
                            ))
                        else:
                            contest = Contest(year=year, host_country=Country.objects.get(id=country_id))  # Is there a better way to go?
                            contest.save()
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"Country with the given ID: {country_id} does not exists in database. First run the 'loadcountry' command or create Country with that ID manually. Skipped."
                        ))

        except Exception as e:
            raise CommandError(f"File '{csv_filename}.csv' does not exist.")

        self.stdout.write(self.style.SUCCESS(
            f"Data was successfully downloaded to the Contest table in database from '{csv_filename}.csv'."))
