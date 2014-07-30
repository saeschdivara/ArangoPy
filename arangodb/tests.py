import unittest
from arangodb.api import Client, Database, Collection, Query
from arangodb.fields import TextField
from arangodb.models import CollectionModel


class ExtendedTestCase(unittest.TestCase):

    def assertDocumentsEqual(self, doc1, doc2):
        """
        """

        for prop in doc1.data:

            doc1_val = doc1.data[prop]
            doc2_val = doc2.data[prop]

            self.assertEqual(doc1_val, doc2_val)


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client(hostname='localhost')

    def tearDown(self):
        pass

    def test_create_and_delete_database(self):

        database_name = 'test_foo_123'

        try:
            db = Database.create(name=database_name)
        except Exception as err:
            self.fail('Create threw execption: %s' % err.message)

        self.assertIsNotNone(db)

        try:
            Database.remove(name=database_name)
        except Exception as err:
            self.fail('Remove threw execption: %s' % err.message)

    def test_get_all_databases(self):
        databases = Database.get_all()

        self.assertTrue(len(databases) >= 1)

        for db in databases:
            self.assertTrue(isinstance(db, Database))


class CollectionTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client(hostname='localhost')
        self.database_name = 'testcase_collection_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_create_and_delete_collection_without_extra_db(self):

        collection_name = 'test_foo_123'

        try:
            col = Collection.create(name=collection_name)
        except Exception as err:
            self.fail('Create threw execption: %s' % err.message)

        self.assertIsNotNone(col)

        try:
            Collection.remove(name=collection_name)
        except Exception as err:
            self.fail('Remove threw execption: %s' % err.message)

    def test_get_collection(self):

        self.client.set_database(name=self.database_name)

        collection_name = 'test_foo_123'

        try:
            col = Collection.create(name=collection_name)
        except Exception as err:
            self.fail('Create threw execption: %s' % err.message)

        self.assertIsNotNone(col)

        retrieved_col = Collection.get_loaded_collection(name=collection_name)

        self.assertEqual(col.id, retrieved_col.id)
        self.assertEqual(col.name, retrieved_col.name)
        self.assertEqual(col.type, retrieved_col.type)

        try:
            Collection.remove(name=collection_name)
        except Exception as err:
            self.fail('Remove threw execption: %s' % err.message)

class AqlQueryTestCase(ExtendedTestCase):

    def setUp(self):
        self.client = Client(hostname='localhost')
        self.database_name = 'testcase_aqlquery_123'
        self.db = Database.create(name=self.database_name)

        self.test_1_col = self.db.create_collection('foo_1')
        self.test_2_col = self.db.create_collection('foo_2')

        self.col1_doc1 = self.test_1_col.create_document()
        self.col1_doc1.set(key='ta', value='fa')
        self.col1_doc1.save()

        self.col2_doc1 = self.test_2_col.create_document()
        self.col2_doc1.set(key='ta', value='fa2')
        self.col2_doc1.save()

    def tearDown(self):

        # They need to be deleted
        Collection.remove(name=self.test_1_col.name)
        Collection.remove(name=self.test_2_col.name)

        Database.remove(name=self.database_name)

    def test_get_all_doc_from_1_collection(self):

        q = Query()
        q.append_collection(self.test_1_col.name)
        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc1 = docs[0]
        self.assertDocumentsEqual(doc1, self.col1_doc1)

class CollectionModelTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client(hostname='localhost')
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

    def test_save_model_with_one_field(self):

        class TestModel(CollectionModel):

            test_field = TextField(is_required=False)

        TestModel.init()

        model = TestModel()
        model.save()

        all_docs = TestModel.collection_instance.documents()
        self.assertEqual(len(all_docs), 1)

        TestModel.destroy()

if __name__ == '__main__':
    unittest.main()