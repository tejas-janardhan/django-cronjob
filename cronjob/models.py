import importlib
import uuid

from crontab import CronItem
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .db_fields import PythonFunctionField, StatusField
from .helper import parse_function_path_string


class Job(models.Model):
    """
    Job model,
    timeout length not used yet.
    """
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = StatusField()

    tags = models.JSONField(default=dict, blank=True)
    timeout_length = models.IntegerField(default=120, null=True)  # sec, none implies no timeout.
    job_path = PythonFunctionField(help_text='Module path followed by the function name. eg. '
                                             'cronjob.jobs.test_function.')

    _args = models.CharField(max_length=100,
                             default='',
                             blank=True,
                             help_text='Enter elements of the array seperated by a comma, e.g. arg1,arg2..argN',
                             verbose_name='args')

    kwargs = models.JSONField(default=dict, blank=True)

    def get_job_function(self):
        module_path, function_name = parse_function_path_string(self.job_path)
        module = importlib.import_module(module_path)
        return getattr(module, function_name)

    def _clean_string(self, string):
        characters_to_remove = ["\'", '\"']
        for ctr in characters_to_remove:
            string = string.replace(ctr, '')
        return string.strip()

    @property
    def args(self):
        if self._args == '':
            return []
        args_string_list = self._args.split(',')
        new_args = []
        for arg in args_string_list:
            try:
                arg = int(arg)
            except ValueError:
                try:
                    arg = float(arg)
                except ValueError:
                    arg = self._clean_string(arg)

            new_args.append(arg)

        return new_args

    def __str__(self):
        return f'{self.name}'

    def is_active(self):
        return self.status == 'Active'


class JobGroupManager(models.Manager):

    def get_active_groups(self):
        return self.get_queryset().filter(status='Active')


class JobGroup(models.Model):
    """
    A group of jobs, it is what dictates the
    """

    duration_choices = (
        ('Minute', 'Minute'),
        ('Hour', 'Hour'),
        ('Day', 'Day'),
        ('Week', 'Week'),
        ('Month', 'Month')
    )

    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = StatusField()

    token = models.UUIDField(default=uuid.uuid4)

    time_duration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000)])
    duration_unit = models.CharField(choices=duration_choices, max_length=100)

    jobs = models.ManyToManyField(Job)

    def get_cron_script(self):

        if self.name is None:
            return ''

        cron_item = CronItem(
            command=f'curl -X POST {settings.DOMAIN_NAME}{reverse("job_group", kwargs={"job_group": self.name, "token": self.token})}')

        if self.duration_unit == 'Minute':
            cron_item.minute.every(self.time_duration)
        elif self.duration_unit == 'Hour':
            cron_item.hour.every(self.time_duration)
        elif self.duration_unit == 'Day':
            cron_item.day.every(self.time_duration)
        elif self.duration_unit == 'Week':
            cron_item.day.every(self.time_duration * 7)
        elif self.duration_unit == 'Month':
            cron_item.month.every(self.time_duration)
        else:
            raise ValueError('Invalid Time Duration')

        return cron_item.render()

    @property
    def time_interval(self):
        return f'{self.time_duration} {self.duration_unit}'

    def __str__(self):
        return f'{self.name} - {self.time_duration} - {self.duration_unit}'

    objects = JobGroupManager()


class JobHistory(models.Model):
    """
    A record of a job executed.
    """

    status_choices = (('Started', 'Job has started.'),
                      ('Timeout', 'No Response'),
                      ('Success', 'Job has succeeded.'),
                      ('Failed', 'Job has failed.'))

    date_started = models.DateTimeField(auto_now_add=True)
    date_ended = models.DateTimeField(default=None, null=True)
    status = models.CharField(choices=status_choices, max_length=100)
    exception = models.TextField(default='')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    job_group = models.ForeignKey(JobGroup, on_delete=models.SET_NULL, null=True)
    time_interval = models.CharField(max_length=100)

    @property
    def duration(self):
        if self.date_ended is None:
            raise ValueError('Job Not Ended')
        time_delta = self.date_ended - self.date_started
        return time_delta.total_seconds()

    def set_success(self):
        self.status = 'Success'
        self.date_ended = timezone.now()
        self.save()

    def set_failure(self, exception_string):
        self.status = 'Failed'
        self.exception = exception_string
        self.date_ended = timezone.now()
        self.save()

    def set_timeout(self):
        self.status = 'Timeout'
        self.date_ended = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.job_group} - {self.job} - {self.status}'
