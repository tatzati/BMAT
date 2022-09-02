from django.core.management.base import BaseCommand

from api.management.commands._private import Ingest


class Command(BaseCommand):
    help = 'Ingest data from csv to postgres'

    def handle(self, *args, **options):
        try:
            ingest = Ingest()
            ingest.handle()

            self.stdout.write("Data imported successfully!")
        except:
            self.stdout.write("An error occurred!")
