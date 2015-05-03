from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from jsonserializermixin import JSONSerializerMixin

def _gt_zero(value):
    """Assumes that we get an int, and if we get an int, attempts to see
    if it is greater than zero.
    """
    if value < 0:
        raise ValidationError(u'{0} is less than zero'.format(value))

class Eggs(models.Model, JSONSerializerMixin):
    """Represents a single day in which a number of chickens can lay a number
    of eggs.
    """
    user = models.ForeignKey(User)
    date = models.DateField('day of the year as a date', unique=True)
    layers = models.IntegerField('number of laying hens', default=0, validators=[_gt_zero])
    eggs = models.IntegerField('number of eggs laid', default=0, validators=[_gt_zero])

    # Must be set to work with the AJAX APIs
    is_ajax_accessible = True

    def describe(self):
        """Provide a simple, JSON-like friendly description of the model.
        
        Also lists the fields that are suitable for passing to the user.
        """
        return {
                    # Means ISO calendar-date (no time) format.
                    "date": "isocalendardate",
                    # Means unsigned integer.
                    "layers": "uint",
                    "eggs": "uint",
                }


class Weight(models.Model, JSONSerializerMixin):
    """Represents a single day in which a human can weigh a certain number of
    pounds.
    """
    user = models.ForeignKey(User)
    date = models.DateField('day of the year as a date', unique=True)
    weight = models.IntegerField('number of pounds', default=0, validators=[_gt_zero])

    # Must be set to work with the AJAX APIs
    is_ajax_accessible = True

    def describe(self):
        """Provide a simple, JSON-like friendly description of the model.
        
        Also lists the fields that are suitable for passing to the user.
        """
        return {
                    # Means ISO calendar-date (no time) format.
                    "date": "isocalendardate",
                    # Means unsigned integer.
                    "weight": "uint",
                }
