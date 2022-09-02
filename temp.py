import csv
import json

from django.core.management.base import BaseCommand
from api.models import Work, Contributor


class Command(BaseCommand):
    help = 'Import csv file from /import/works_metadata.csv'
    valid = []

    def check_iswc(self, dic, value):
        try:
            return dic["iswc"] == value
        except KeyError:
            return False

    def handle(self, *args, **options):
        file_path = "/app/import/works_metadata.csv"

        with open(file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # check record for invalid values
                title = row["title"]
                if not title:
                    # discard record if no title is present
                    continue

                contributors = list(row["contributors"].split("|"))
                if not contributors:
                    # discard record if no contributors are present
                    continue

                iswc = row["iswc"]
                # check that iswc exists, otherwise take title and first contributor
                if not iswc:
                    if not contributors:
                        self.stdout.write(f"No contributors for this record {row}")
                        break
                    iswc = f"{title},{contributors[0]}"
                    row["iswc"] = iswc

                possible_duplicate_data = f"{title},{contributors[0]}"
                if any(f"{dic['title']},{dic['contributor'][0]}" == possible_duplicate_data for dic in self.valid):
                    pass

                if any(iswc == dic.get("iswc", None) for dic in self.valid):
                    # check if contributors differ to take their union
                    contributors_from_dict = row["contributors"]
                    if set(contributors_from_dict) == set(contributors):
                        continue
                    results_list = [contributors_from_dict, contributors]
                    results_union = set().union(*results_list)
                    results_union = list(results_union)

                    row["contributors"] = results_union
                else:
                    row["contributors"] = contributors

                self.valid.append(row)
                self.stdout.write(json.dumps(row))

            self.stdout.write("======================================================================================")
            self.stdout.write(json.dumps(self.valid))
