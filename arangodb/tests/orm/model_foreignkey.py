import unittest

from arangodb.api import Database
from arangodb.orm.fields import CharField, ForeignKeyField
from arangodb.orm.models import CollectionModel


class CollectionModelForeignKeyFieldTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_collection_model_foreign_key_field_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_foreign_key_field(self):

        class ForeignTestModel(CollectionModel):

            test_field = CharField(required=True)

        class TestModel(CollectionModel):

            other = ForeignKeyField(to=ForeignTestModel, required=True)

        # Init collections
        ForeignTestModel.init()
        TestModel.init()

        # Init models
        model_1 = ForeignTestModel()
        model_1.test_field = 'ddd'

        model_2 = TestModel()
        model_2.other = model_1

        # Save models
        model_1.save()
        model_2.save()

        all_test_models = TestModel.objects.all()
        self.assertEqual(len(all_test_models), 1)

        real_model = all_test_models[0]

        self.assertEqual(real_model.other.test_field, model_1.test_field)

        # Destroy collections
        ForeignTestModel.destroy()
        TestModel.destroy()