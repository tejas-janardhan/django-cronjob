import importlib

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from cronjob.helper import parse_function_path_string


@deconstructible
class FunctionValidator:
    message = 'Invalid function path %(value)s'
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """
        Validate that the input contains (or does *not* contain, if
        inverse_match is True) a match for the regular expression.
        """

        module_path, _ = parse_function_path_string(value)

        try:
            importlib.import_module(module_path)
        except ModuleNotFoundError:
            raise ValidationError(self.message, code=self.code, params={'value': value})