from django.test import TestCase

from .models import JobGroup, Job, JobHistory


# Create your tests here.

class TestJobModel(TestCase):

    def setUp(self):
        self.job = Job.objects.create()


class TestJobGroupModel(TestCase):
    pass


class TestJobHistoryModel(TestCase):
    pass
