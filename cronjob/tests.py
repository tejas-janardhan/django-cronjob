from django.test import TestCase

from .models import JobGroup, Job, JobHistory


def test_job_no_args_no_kwargs():
    pass


def test_job(arg1, arg2, kwarg1=None, kwarg2=None):
    pass


# Create your tests here.

class TestJobModel(TestCase):

    def setUp(self):
        self.job1 = Job.objects.create(name='TestJob1',
                                       job_path='cronjob.tests.test_job_no_args_no_kwargs',
                                       tags={'Tag1': 'Val1',
                                             'Tag2': 'Val2'})

        self.job2 = Job.objects.create(name='TestJob2',
                                       job_path='cronjob.tests.test_job_no_args_no_kwargs',
                                       status='Inactive',
                                       tags={'Tag1': 'Val1',
                                             'Tag2': 'Val2'},
                                       _args='3,"Test"',
                                       kwargs={'kwarg1': None,
                                               'kwarg2': None})

    def test_get_job_function(self):
        self.assertEqual(self.job1.get_job_function(), test_job_no_args_no_kwargs)

    def test_clean_string(self):
        self.assertEqual(self.job1._clean_string('\'FF\"'), 'FF')

    def test_args(self):
        self.assertEqual(self.job1.args, [])
        self.assertEqual(self.job2.args, [3, 'Test'])

    def test_is_active(self):
        self.assertEqual(self.job1.is_active(), True)
        self.assertEqual(self.job2.is_active(), False)


class TestJobGroupModel(TestCase):

    def setUp(self):
        self.jobGroup1 = JobGroup.objects.create(name='TestJobGroup1',
                                                 time_duration=10,
                                                 duration_unit='Minute')

    def test_cron_script(self):
        self.assertEqual(self.jobGroup1.get_cron_script(),
                         '*/10 * * * * curl -X POST 127.0.0.1:8000/cronjob/TestJobGroup1/38eb41a8-de58-4238-8a43-07223d424c1e')

    def test_time_interval(self):
        self.assertEqual(self.jobGroup1.time_interval, 'INSERT TIME INTERVAL')


class TestJobHistoryModel(TestCase):

    def setUp(self):
        self.jobHistory1 = JobHistory.objects.create()

    def test_duration(self):
        self.jobHistory1.set_success()
        self.assertEqual(self.jobHistory1.duration, 'Add stuff here')

    def test_set_success(self):
        self.jobHistory1.set_success()
        self.assertEqual(self.jobHistory1.status, 'Success')

    def test_set_failure(self):
        self.jobHistory1.set_failure(exception_string='TestException')
        self.assertEqual(self.jobHistory1.status, 'Failed')
        self.assertEqual(self.jobHistory1.exception, 'TestException')

    def test_set_time_out(self):
        self.jobHistory1.set_timeout()
        self.assertEqual(self.jobHistory1.status, 'Timeout')
