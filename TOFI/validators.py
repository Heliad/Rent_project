from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as laz


def validate_age(value):
    if value > 100:
        raise ValidationError(
            laz('%(value)s is not an age'),
            params={'value': value},
        )