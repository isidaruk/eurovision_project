import csv

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from artists.models import Artist
from contests.models import Contest
from countries.models import Country
from participants.models import Participant


class Command(BaseCommand):
    help = 'Loads a data to the Participant table in the database from the specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The CSV file to load data from')

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']

        try:
            with open(f'{csv_filename}', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                next(csv_reader)  # The first line is the header, loop over the first line.

                for artist_id, contest_id, country_id, song in csv_reader:
                    # Check if there is any data.
                    if not (artist_id and contest_id and country_id and song):
                        self.stdout.write(self.style.WARNING(f"There are some data missing {artist_id, contest_id, country_id, song}."))

                    else:
                        # If there is Contest, we should check if there is a Country_ID and Artist_ID in db.
                        if Contest.objects.filter(id=contest_id).exists():

                            # Maybe the better way to check it separetely.
                            if Country.objects.filter(id=country_id).exists() and Artist.objects.filter(id=artist_id).exists():
                                artist = Artist.objects.get(id=artist_id)
                                contest = Contest.objects.get(id=contest_id)
                                country = Country.objects.get(id=country_id)

                                if Participant.objects.all().filter(artist=artist_id, contest=contest_id, country=country_id):
                                    self.stdout.write(self.style.WARNING(
                                        f"This record ({artist.name} - {song} - {country.name} - {contest.year}) already in db. Skipped."))

                                else:
                                    # Save if validation was passed.
                                    p = Participant(artist=artist, contest=contest, country=country, song=song)
                                    p.save()

                                    self.stdout.write(self.style.SUCCESS(
                                        f"Data ({artist.name} - {song} - {country.name} - {contest.year}) was successfully saved to the Particpant table in database.")
                                    )

                            else:
                                self.stdout.write(
                                    self.style.WARNING(f"The Country or Artist with the IDs {country_id, artist_id} respectively do not exists in database. Skipped.")
                                )

                        else:
                            self.stdout.write(self.style.WARNING(f"The Contest with the ID {contest_id} does not exists in database. Skipped."))

        except Exception as e:
            raise CommandError(f"File '{csv_filename}' does not exist.")

        self.stdout.write(self.style.SUCCESS(
            f"Done. Successfully loaded data from '{csv_filename}'."))
