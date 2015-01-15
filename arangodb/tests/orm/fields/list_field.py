import unittest
from arangodb.api import Database
from arangodb.orm.fields import ListField
from arangodb.orm.models import CollectionModel


class ListFieldTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'test_case_list_field_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_field_not_null_without_default(self):

        class TestModel(CollectionModel):

            list_field = ListField(null=False)

        # Init collections
        TestModel.init()

        # Create model
        model = TestModel()
        model.list_field = 13, 15, 16
        model.save()

        documents = TestModel.collection_instance.documents()
        self.assertEqual(len(documents), 1)

        doc1 = documents[0]
        self.assertTrue(isinstance(doc1.list_field, list))

        # Destroy
        TestModel.destroy()

    def test_field_with_special_values(self):

        class TestModel(CollectionModel):

            list_field = ListField(null=False)

        # Init collections
        TestModel.init()

        # Create model
        model = TestModel()
        model.list_field = 13, {'test': 'foo'}, [50, 60]
        model.save()

        documents = TestModel.collection_instance.documents()
        self.assertEqual(len(documents), 1)

        doc1 = documents[0]
        self.assertTrue(isinstance(doc1.list_field, list))

        self.assertEqual(len(doc1.list_field), 3)

        val1 = doc1.list_field[0]
        val2 = doc1.list_field[1]
        val3 = doc1.list_field[2]

        self.assertTrue(isinstance(val1, int))
        self.assertTrue(isinstance(val2, dict))
        self.assertTrue(isinstance(val3, list))

        # Destroy
        TestModel.destroy()