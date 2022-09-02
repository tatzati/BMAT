from django.test import TestCase
from rest_framework.test import APIClient

from api.management.commands._private import Ingest
from api.models import Work, Contributor


# Create your tests here.
class TaskTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TaskTestCase, cls).setUpClass()
        # run management command here
        ingest = Ingest()
        ingest.handle()

    def test_for_works(self):
        works = Work.objects.filter(is_deleted=False)
        self.assertEqual(len(works), 4)

    def test_first_work(self):
        work = Work.objects.get(iswc="T9204649558")
        self.assertEqual(work.iswc, "T9204649558")
        self.assertEqual(work.title, "Shape of You")
        self.assertEqual(work.contributors.count(), 1)

    def test_for_contributors(self):
        contributors = Contributor.objects.filter(is_deleted=False)
        self.assertEqual(contributors.count(), 9)

    def test_correct_payload(self):
        client = APIClient()
        correct_payload = {"iswc": ["T9204649558"]}
        response = client.post('/works/enrich', correct_payload, format='json')
        assert response.status_code == 200

    def test_incorrect_payload(self):
        client = APIClient()
        incorrect_payload = {"iswc": ["T94649558"]}
        response = client.post('/works/enrich', incorrect_payload, format='json')
        assert response.status_code == 200
