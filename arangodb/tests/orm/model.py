import unittest

from arangodb.api import Database
from arangodb.index.unique import HashIndex
from arangodb.orm.fields import CharField
from arangodb.orm.models import CollectionModel


class CollectionModelTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_collection_model_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_init_and_delete_collection_model(self):

        class TestModel(CollectionModel):
            pass

        TestModel.init()
        model_collection_name = TestModel.collection_instance.name

        self.assertEqual(model_collection_name, "TestModel")

        TestModel.destroy()

    def test_own_name_init_and_delete(self):

        class TestModel(CollectionModel):
            collection_name = "test_model"

        TestModel.init()
        model_collection_name = TestModel.collection_instance.name

        self.assertEqual(model_collection_name, "test_model")

        TestModel.destroy()

    def test_empty_name(self):

        class TestModel(CollectionModel):
            collection_name = ""

        TestModel.init()

        model_collection_name = TestModel.collection_instance.name

        self.assertEqual(model_collection_name, "TestModel")

        TestModel.destroy()

    def test_get_model_key_and_id_directly(self):

        class TestModel(CollectionModel):
            collection_name = "test_model"

        TestModel.init()

        model = TestModel()
        model.save()

        self.assertEqual(model.key, model.document.key)
        self.assertEqual(model.id, model.document.id)

        TestModel.destroy()

    def test_save_model_with_one_field_not_required(self):

        class TestModel(CollectionModel):

            test_field = CharField(required=False)

        TestModel.init()

        model_1 = TestModel()

        model_2 = TestModel()
        model_2.test_field = "model_2_text"

        model_1.save()
        model_2.save()

        all_docs = TestModel.collection_instance.documents()
        self.assertEqual(len(all_docs), 2)

        retrieved_model_1 = None
        retrieved_model_2 = None

        for doc in all_docs:
            if doc.key == model_2.document.key:
                retrieved_model_2 = doc
            else:
                retrieved_model_1 = doc

        if retrieved_model_1:
            self.assertEqual(retrieved_model_1.get('test_field'), None)
        if retrieved_model_2:
            self.assertEqual(retrieved_model_2.get('test_field'), "model_2_text")

        TestModel.destroy()

    def test_save_model_with_one_field_required(self):

        class TestModel(CollectionModel):

            test_field = CharField(required=True)

        TestModel.init()

        model_1 = TestModel()

        model_2 = TestModel()
        model_2.test_field = "model_2_text"

        try:
            model_1.save()
            self.assertTrue(False, 'Save needs to throw an exception because field is required and not set')
        except:
            pass

        model_2.save()

        all_docs = TestModel.collection_instance.documents()
        self.assertEqual(len(all_docs), 2)

        retrieved_model_1 = None
        retrieved_model_2 = None

        for doc in all_docs:
            if doc.key == model_2.document.key:
                retrieved_model_2 = doc
            else:
                retrieved_model_1 = doc

        if retrieved_model_1:
            self.assertEqual(retrieved_model_1.get('test_field'), None)
        if retrieved_model_2:
            self.assertEqual(retrieved_model_2.get('test_field'), "model_2_text")

        TestModel.destroy()

    def test_field_has_its_own_name(self):

        class TestModel(CollectionModel):

            test_field = CharField(required=True)

        TestModel.init()

        self.assertEqual(TestModel.test_field.name, 'test_field')

        TestModel.destroy()

    def test_hash_index_on_model_field(self):

        class TestModel(CollectionModel):

            username_hash_index = HashIndex(fields=['username'])

            username = CharField(required=True, null=False)

        TestModel.init()

        has_exception = False

        try:
            model1 = TestModel()
            model1.username = 'aoo'
            model1.save()

            model2 = TestModel()
            model2.username = 'aoo'
            model2.save()
        except:
            has_exception = True

        self.assertTrue(has_exception)

        all_created_models = TestModel.objects.all()

        self.assertEqual(len(all_created_models), 1)

        TestModel.destroy()
