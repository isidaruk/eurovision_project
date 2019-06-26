import csv

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from artists.models import Artist


class Command(BaseCommand):
    help = 'Loads a data to the Artist table in the database from the specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The CSV file to load data from')

    def process_file(self, reader):
        for line in reader:
            artist = line[1]

            # Check to see if artist is already in database.
            if Artist.objects.filter(name=artist).exists():
                self.stdout.write(self.style.WARNING(
                    f"Name: '{artist}' is already exists in the Artist table in database. Skipped."
                ))
            else:
                a = Artist(name=artist)
                a.save()

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
                f"Successfully downloaded data to the Artist table in database from '{csv_filename}'."
            ))
        else:
            self.stdout.write(self.style.WARNING('The input file is empty'))
