from django.db import models
from .validators import FunctionValidator


class PythonFunctionField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.update({'max_length': 100})
        super().__init__(*args, **kwargs)
        self.validators.append(FunctionValidator())


class StatusField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.update({'choices': (
            ('Active', 'Active'),
            ('Inactive', 'Inactive')
        ), 'max_length': 100})

        super().__init__(*args, **kwargs)
