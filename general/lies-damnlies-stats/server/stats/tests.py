"""
Automated tests for the ldls application.
"""

import json
from datetime import datetime
from django.utils import unittest
from django.db import models
from jsonserializermixin import JSONSerializerMixin
from jsonencoderdelegator import JSONEncoderDelegator



class TestModel(models.Model, JSONSerializerMixin):
    """A sample test model.
    """
    count = models.IntegerField()

class TestRelatedModel(models.Model, JSONSerializerMixin):
    """A sample model related to the test model.
    """
    owner = models.ForeignKey(TestModel)
    description = models.TextField()

class TestDescribedModel(models.Model, JSONSerializerMixin):
    """A sample model related to the test model, but doesn't describe the
    relation.
    """
    owner = models.ForeignKey(TestModel)
    description = models.TextField()
    def describe(self):
        """Testing out the whitelist for only the description.
        """
        return {
                    "description": "string",
                }


class JSONSerializerMixinTest(unittest.TestCase):
    """Test the json serializer mixin, ensure that it returns a JSON
    friendly object.
    """
    def setUp(self):
        self.t = TestModel.objects.create(count=42)
        self.d = TestDescribedModel.objects.create(owner=self.t, description=24)
    def tearDown(self):
        self.d.delete()
        self.t.delete()

    def test_sanity(self):
        self.assertEqual(self.t.tojsonobject(), 
                         {"count": 42, "id": 1},
                         "Serialized model matches JSON friendly object.")
        
        self.assertEqual(json.dumps(self.t.tojsonobject(), sort_keys=True),
                         '{"count": 42, "id": 1}',
                         "Serialized model behaves correctly in json.dumps.")
    
    def test_describe(self):
        self.assertEqual(self.d.tojsonobject(),
                         {"description": "24"},
                         "White list correctly ignores the owner attribute.")



class JSONEncoderDelegatorTest(unittest.TestCase):
    def setUp(self):
        self.testlist = [TestModel.objects.create(count=42),
                         TestModel.objects.create(count=42),]
        
        self.relatedTestModel = TestRelatedModel.objects.create(
                                    owner=self.testlist[0],
                                    description="42"
                                )
        
    def tearDown(self):
        # Remove models with relations, first.
        self.relatedTestModel.delete()
        del self.relatedTestModel
        
        # Remove non related models.
        for t in self.testlist:
            t.delete()
        del self.testlist

    def test_sanity(self):
        # Expected iterators work as expected.
        testobject = [42, 42]
        json = JSONEncoderDelegator()
        output = json.encode(testobject)
        self.assertEqual(output, 
                         "[42, 42]",
                         "Standard items serialized correctly.")
        
    def test_list(self):
        json = JSONEncoderDelegator()
        output = json.encode(self.testlist)
        self.assertEqual(output, 
                         '[{"count": 42, "id": 1}, {"count": 42, "id": 2}]',
                         "jsonserializer in a list works as expected.")
    
    def test_related(self):
        self.assertEqual(self.relatedTestModel.tojsonobject(),
                         {'owner': {'fk': 1}, 'id': 1, 'description': u'42'},
                         "Models return a simple object with related fk.")
