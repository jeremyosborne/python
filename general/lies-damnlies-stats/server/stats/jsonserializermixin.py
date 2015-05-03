'''
# Basic usage
from jsonserializermixin import JSONSerializerMixin
# Then at model definition time

class TestModel(models.Model, JSONSerializerMixin):
    # Do your class...
    pass
'''

import json
from django.db.models import Model
from django.db.models.query import QuerySet



# Mappings of various Django fields to 
fields = {
    "boolean": ['BooleanField', 'NullBooleanField'],
    "int": ['IntegerField', 'AutoField', 'PositiveSmallIntegerField'],
    "float": ['DecimalField', 'FloatField'],
}

class JSONSerializerMixin(object):
    """Mixin for Django models.
    
    Impements .tojsonobject() method.
    
    Accesses .describe() method if the model implements it. Assumes the
    .describe() method returns a dictionary which acts as a white list of
    keys allowed in the output.
    """
    
    # All models are treated as dictionary types.
    _jsonobject = None

    def tojsonobject(self):
        """Main interface method used to work with a JSON encoder.
        """
        # Initialize the dictionary object.
        self._jsonobject = {}

        self._handle_model(self)

        # Okay to return, as we'll create a new object on each call.
        return self._jsonobject
    
    def _handle_model(self, mod):
        """Called to handle a django Model.
        """
        field_whitelist = None
        if hasattr(self, "describe"):
            # assume that describe returns a dict.
            field_whitelist = self.describe()
        
        for field in mod._meta.local_fields:
            if not field_whitelist or (field_whitelist and field.name in field_whitelist):
                if field.rel is None:
                    self._handle_field(mod, field)
                else:
                    self._handle_fk_field(mod, field)

        for field in mod._meta.many_to_many:
            if not field_whitelist or (field_whitelist and field.name in field_whitelist):
                self._handle_m2m_field(mod, field)

    def _handle_field(self, mod, field):
        """Called to handle each individual (non-relational) field on an 
        object.
        """
        if field.get_internal_type() in fields["boolean"]:
            if field.value_to_string(mod) == 'True':
                self._jsonobject[field.name] = True
            elif field.value_to_string(mod) == 'False':
                self._jsonobject[field.name] = False
            else:
                self._jsonobject[field.name] = None
        elif field.get_internal_type() in fields["int"]:
            # Take care of the instance of None
            if field.value_to_string(mod) != 'None':
                self._jsonobject[field.name] = int(field.value_to_string(mod))
            else:
                self._jsonobject[field.name] = None
        elif field.get_internal_type() in fields["float"]:
                self._jsonobject[field.name] = float(field.value_to_string(mod))
        else:
            self._jsonobject[field.name] = field.value_to_string(mod)

    def _handle_fk_field(self, mod, field):
        """Called to handle a ForeignKey field.
        """
        related = getattr(mod, field.name)
        if related is not None:
            if field.rel.field_name == related._meta.pk.name:
                # Related to remote object via primary key
                fk = related._get_pk_val()
            else:
                # Related to remote object via other field
                fk = getattr(related, field.rel.field_name)
            d = {
                    'fk': fk,
                }
            if hasattr(related, 'natural_key'):
                d.update({'natural_key': related.natural_key()})

            self._jsonobject[field.name] = d

    def _handle_m2m_field(self, mod, field):
        """Called to handle a ManyToManyField.
        """
        raise NotImplementedError("Please implement _handle_m2m_field.")
        
