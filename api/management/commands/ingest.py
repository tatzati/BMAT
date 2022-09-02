from django.core.management.base import BaseCommand

from api.management.commands._private import Ingest


class Command(BaseCommand):
    help = 'Ingest data from csv to postgres'

    def handle(self, *args, **options):
        ingest = Ingest()
        ingest.handle()
