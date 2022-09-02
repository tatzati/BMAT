import csv

from django.db import IntegrityError
from django.db.transaction import atomic

from api.models import Work, Contributor


class Ingest:
    valid_list_of_works = []

    def handle(self):
        file_path = "/app/import/works_metadata.csv"
        valid_dict = {}
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)
            for row in csv_reader:
                title = row[0]
                contributors = list(row[1].split("|"))
                iswc = row[2]

                # discard the row if no contributors and title present
                if not contributors and not title:
                    break

                # check that iswc exists, otherwise take title and first contributor
                if not iswc:
                    iswc = f"{title},{contributors[0]}"

                # check that title and first contributor is not the same
                possible_old_key = f"{title},{contributors[0]}"
                if possible_old_key in valid_dict:
                    # this means that the song is included, but it doesn't have an iswc, so we change the key to iswc
                    verified_old_key = possible_old_key
                    valid_dict[iswc] = valid_dict.pop(verified_old_key)

                if iswc in valid_dict:
                    # check if contributors differ to take their union
                    contributors_from_dict = valid_dict[iswc][1]
                    if set(contributors_from_dict) == set(contributors):
                        break
                    results_list = [contributors_from_dict, contributors]
                    results_union = set().union(*results_list)
                    results_union = list(results_union)
                    valid_dict[iswc] = (title, results_union)
                else:
                    valid_dict[iswc] = (title, contributors)

            self.transform_dictionary(valid_dict)

        self.insert_to_db()

    def transform_dictionary(self, valid_dict):
        for key, value in valid_dict.items():
            result = {"iswc": key, "title": value[0], "contributors": value[1]}
            self.valid_list_of_works.append(result)

    @atomic
    def insert_to_db(self):
        for data_dic in self.valid_list_of_works:
            obj_list = [Contributor(name=contributor) for contributor in data_dic.get("contributors")]
            try:
                contributor_objs = Contributor.objects.bulk_create(obj_list)
                data_dic.pop("contributors")
                work_obj = Work(**data_dic)
                work_obj.save()
                work_obj.contributors.set(contributor_objs)
            except IntegrityError:
                continue
