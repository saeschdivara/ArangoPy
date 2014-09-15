import unittest

from arangodb.api import Client, Database, Collection, Document
from arangodb.orm.fields import CharField, ForeignKeyField
from arangodb.orm.models import CollectionModel
from arangodb.query.advanced import Query
from query.simple import SimpleQuery
from transaction.controller import Transaction, TransactionController


client = Client(hostname='localhost')

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
        pass

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
        self.database_name = 'testcase_collection_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_create_and_delete_collection_without_extra_db(self):

        collection_name = 'test_foo_123'

        try:
            col = Collection.create(name=collection_name)
        except Exception as err:
            self.fail('Create threw exception: %s' % err.message)

        self.assertIsNotNone(col)

        try:
            Collection.remove(name=collection_name)
        except Exception as err:
            self.fail('Remove threw exception: %s' % err.message)

    def test_get_collection(self):

        collection_name = 'test_foo_123'

        try:
            col = Collection.create(name=collection_name)
        except Exception as err:
            self.fail('Create threw exception: %s' % err.message)

        self.assertIsNotNone(col)

        retrieved_col = Collection.get_loaded_collection(name=collection_name)

        self.assertEqual(col.id, retrieved_col.id)
        self.assertEqual(col.name, retrieved_col.name)
        self.assertEqual(col.type, retrieved_col.type)

        try:
            Collection.remove(name=collection_name)
        except Exception as err:
            self.fail('Remove threw exception: %s' % err.message)


class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_document_access_values_by_attribute_getter(self):
        doc = Document(id='', key='', collection='', api=client.api)
        # set this to true so it won't make requests to nothing
        doc.is_loaded = True
        doc_attr_value = 'foo_bar'
        doc.set(key='test', value=doc_attr_value)

        self.assertEqual(doc.test, doc_attr_value)

    def test_document_access_values_by_attribute_setter(self):
        doc = Document(id='', key='', collection='', api=client.api)
        # set this to true so it won't make requests to nothing
        doc.is_loaded = True
        doc_attr_value = 'foo_bar'

        doc.test = doc_attr_value

        self.assertEqual(doc.get(key='test'), doc_attr_value)


class AqlQueryTestCase(ExtendedTestCase):
    def setUp(self):
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


class SimpleQueryTestCase(ExtendedTestCase):
    def setUp(self):
        self.database_name = 'testcase_simple_query_123'
        self.db = Database.create(name=self.database_name)

        # Create test data
        self.test_1_col = self.db.create_collection('foo_1')
        self.test_2_col = self.db.create_collection('foo_2')

        self.col1_doc1 = self.test_1_col.create_document()
        self.col1_doc1.ta='fa'
        self.col1_doc1.save()

        self.col1_doc2 = self.test_1_col.create_document()
        self.col1_doc2.ta='fa'
        self.col1_doc2.save()

        self.col2_doc1 = self.test_2_col.create_document()
        self.col2_doc1.save()

    def tearDown(self):
        # They need to be deleted
        Collection.remove(name=self.test_1_col.name)
        Collection.remove(name=self.test_2_col.name)

        Database.remove(name=self.database_name)

    def test_get_document_by_example(self):
        uid = self.col1_doc1.key
        doc = SimpleQuery.get_by_example(collection=self.test_1_col, example_data={
            '_key': uid,
        })

        self.assertDocumentsEqual(doc, self.col1_doc1)

    def test_get_all_documents(self):

        docs = SimpleQuery.all(collection=self.test_1_col)

        self.assertEqual(len(docs), 2)

        doc1 = docs[0]
        doc2 = docs[1]

        self.assertNotEqual(doc1, doc2)


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
            if doc.get(key='_key') == model_1.document.get(key='_key'):
                retrieved_model_1 = doc
            else:
                retrieved_model_2 = doc

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
            if doc.get(key='_key') == model_1.document.get(key='_key'):
                retrieved_model_1 = doc
            else:
                retrieved_model_2 = doc

        if retrieved_model_1:
            self.assertEqual(retrieved_model_1.get('test_field'), None)
        if retrieved_model_2:
            self.assertEqual(retrieved_model_2.get('test_field'), "model_2_text")

        TestModel.destroy()


class CollectionModelForeignKeyFieldTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_foreign_key_field_123'
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


class TransactionTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_collection(self):
        trans = Transaction(collections=[])
        
        ctrl = TransactionController()

        ctrl.start(transaction=trans)

if __name__ == '__main__':
    unittest.main()