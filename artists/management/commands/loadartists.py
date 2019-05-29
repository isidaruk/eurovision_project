from django.core.management.base import BaseCommand, CommandError

import csv

from artists.models import Artist


class Command(BaseCommand):
    help = 'Loads a data to the Artist table in the database from the specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The CSV file to load data from')

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']

        try:
            with open(f'{csv_filename}', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                next(csv_reader)  # The first linie is the header, loop over the first line.

                for line in csv_reader:
                    artist_name = line[1]

                    # Check to see if country is already in database.
                    if Artist.objects.filter(name=artist_name).exists():
                        self.stdout.write(self.style.WARNING(
                            f"Some data (field Name: {artist_name}) is already exists in the Artist table in database. Skipped."
                        ))
                    else:
                        a = Artist(name=artist_name)
                        a.save()

        except Exception as e:
            raise CommandError(f"File '{csv_filename}' does not exist.")

        self.stdout.write(self.style.SUCCESS(
            f"Data was successfully downloaded to the Artist table in database from '{csv_filename}'."))
