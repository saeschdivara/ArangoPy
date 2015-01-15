import unittest

from arangodb.api import Database
from arangodb.orm.fields import DictField
from arangodb.orm.models import CollectionModel


class DictFieldTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'test_case_dict_field_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_field_not_null_without_default(self):

        class TestModel(CollectionModel):

            dict_field = DictField(null=False)

        # Init collections
        TestModel.init()

        # Create model
        model = TestModel()
        model.dict_field = {
            'test_1': 'foo',
            'test_2': 'bar',
        }
        model.save()

        documents = TestModel.collection_instance.documents()
        self.assertEqual(len(documents), 1)

        doc1 = documents[0]
        self.assertTrue(isinstance(doc1.dict_field, dict))

        self.assertTrue('test_1' in doc1.dict_field)
        self.assertEqual(doc1.dict_field['test_1'], 'foo')

        self.assertTrue('test_2' in doc1.dict_field)
        self.assertEqual(doc1.dict_field['test_2'], 'bar')

        # Destroy
        TestModel.destroy()

    def test_field_with_special_values(self):

        class TestModel(CollectionModel):

            dict_field = DictField(null=False)

        # Init collections
        TestModel.init()

        # Create model
        model = TestModel()
        model.dict_field = {
            'number': 13,
            'a_dict': {'test': 'foo'},
            'a_list': [50, 60]
        }
        model.save()

        documents = TestModel.collection_instance.documents()
        self.assertEqual(len(documents), 1)

        doc1 = documents[0]
        self.assertTrue(isinstance(doc1.dict_field, dict))

        self.assertEqual(len(doc1.dict_field.keys()), 3)

        val1 = doc1.dict_field['number']
        val2 = doc1.dict_field['a_dict']
        val3 = doc1.dict_field['a_list']

        self.assertTrue(isinstance(val1, int))
        self.assertTrue(isinstance(val2, dict))
        self.assertTrue(isinstance(val3, list))

        # Destroy
        TestModel.destroy()