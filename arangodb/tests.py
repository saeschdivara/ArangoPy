import unittest
import datetime

from arangodb.api import Client, Database, Collection, Document
from arangodb.orm.fields import CharField, ForeignKeyField, NumberField, DatetimeField, DateField
from arangodb.orm.models import CollectionModel
from arangodb.query.advanced import Query, Traveser
from arangodb.query.utils.document import create_document_from_result_dict
from arangodb.query.simple import SimpleQuery
from arangodb.transaction.controller import Transaction, TransactionController
from arangodb.user import User


client = Client(hostname='localhost')

class ExtendedTestCase(unittest.TestCase):
    def assertDocumentsEqual(self, doc1, doc2):
        """
        """

        self.assertEqual(doc1.id, doc2.id)

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

        db = Database.create(name=database_name)

        self.assertIsNotNone(db)

        Database.remove(name=database_name)

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

        col = Collection.create(name=collection_name)

        self.assertIsNotNone(col)

        Collection.remove(name=collection_name)

    def test_get_collection(self):

        collection_name = 'test_foo_123'

        col = Collection.create(name=collection_name)

        self.assertIsNotNone(col)

        retrieved_col = Collection.get_loaded_collection(name=collection_name)

        self.assertEqual(col.id, retrieved_col.id)
        self.assertEqual(col.name, retrieved_col.name)
        self.assertEqual(col.type, retrieved_col.type)

        Collection.remove(name=collection_name)


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
        self.col1_doc1.little_number = 33
        self.col1_doc1.loved = False
        self.col1_doc1.small_text = "lll aa"
        self.col1_doc1.save()

        self.col1_doc2 = self.test_1_col.create_document()
        self.col1_doc2.little_number = 1
        self.col1_doc2.loved = False
        self.col1_doc2.small_text = "aaa aa"
        self.col1_doc2.save()

        self.col1_doc3 = self.test_1_col.create_document()
        self.col1_doc3.little_number = 3
        self.col1_doc3.loved = True
        self.col1_doc3.small_text = "xxx tt"
        self.col1_doc3.save()

        self.col2_doc1 = self.test_2_col.create_document()
        self.col2_doc1.little_number = 33
        self.col2_doc1.loved = False
        self.col2_doc1.save()

        self.col2_doc2 = self.test_2_col.create_document()
        self.col2_doc2.little_number = 11
        self.col2_doc2.loved = True
        self.col2_doc2.save()

    def tearDown(self):
        # They need to be deleted
        Collection.remove(name=self.test_1_col.name)
        Collection.remove(name=self.test_2_col.name)

        Database.remove(name=self.database_name)

    def test_get_all_doc_from_1_collection(self):
        q = Query()
        q.append_collection(self.test_2_col.name)
        docs = q.execute()

        self.assertEqual(len(docs), 2)

    def test_filter_number_field_in_document(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(little_number=self.col1_doc3.little_number)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc = docs[0]
        self.assertDocumentsEqual(doc, self.col1_doc3)

    def test_filter_string_field_in_document(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(small_text=self.col1_doc2.small_text)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc = docs[0]
        self.assertDocumentsEqual(doc, self.col1_doc2)

    def test_filter_from_multiple_collections(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.append_collection(self.test_2_col.name)

        dynamic_filter_dict = {}
        col_1_filter_name = "%s__%s" % (self.test_1_col.name, "little_number")
        col_2_filter_name = "%s__%s" % (self.test_2_col.name, "little_number")

        dynamic_filter_dict[col_1_filter_name] = 33
        dynamic_filter_dict[col_2_filter_name] = 33
        q.filter(bit_operator=Query.OR_BIT_OPERATOR, **dynamic_filter_dict)

        docs = q.execute()

        self.assertEqual(len(docs), 2)

        doc1 = docs[0]
        doc2 = docs[1]

        self.assertNotEqual(doc1.id, doc2.id)

        self.assertEqual(doc1.little_number, 33)
        self.assertEqual(doc2.little_number, 33)

    def test_exclude_document_from_list(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.exclude(loved=False)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc1 = docs[0]

        self.assertDocumentsEqual(doc1, self.col1_doc3)

    def test_sorting_asc_document_list(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.order_by('little_number')

        docs = q.execute()

        self.assertEqual(len(docs), 3)

        doc1 = docs[0]
        doc2 = docs[1]
        doc3 = docs[2]

        self.assertDocumentsEqual(doc1, self.col1_doc2)
        self.assertDocumentsEqual(doc2, self.col1_doc3)
        self.assertDocumentsEqual(doc3, self.col1_doc1)


class SimpleQueryTestCase(ExtendedTestCase):
    def setUp(self):
        self.database_name = 'testcase_simple_query_123'
        self.db = Database.create(name=self.database_name)

        # Create test data
        self.test_1_col = self.db.create_collection('foo_1')
        self.test_2_col = self.db.create_collection('foo_2')

        self.col1_doc1 = self.test_1_col.create_document()
        self.col1_doc1.ta='fa'
        self.col1_doc1.bla='aaa'
        self.col1_doc1.save()

        self.col1_doc2 = self.test_1_col.create_document()
        self.col1_doc2.ta='fa'
        self.col1_doc2.bla='xxx'
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

    def test_get_no_document(self):
        doc = SimpleQuery.get_by_example(collection=self.test_1_col, example_data={
            '_key': 'dddd',
        })

        self.assertEqual(doc, None)

    def test_get_all_documents(self):

        docs = SimpleQuery.all(collection=self.test_1_col)

        self.assertEqual(len(docs), 2)

        doc1 = docs[0]
        doc2 = docs[1]

        self.assertNotEqual(doc1, doc2)

    def test_update_document(self):
        SimpleQuery.update_by_example(collection=self.test_1_col, example_data={ 'bla': 'xxx' }, new_value={
            'bla': 'ttt'
        })

        self.col1_doc2.retrieve()

        self.assertEqual(self.col1_doc2.bla, 'ttt')

    def test_replace_document(self):
        SimpleQuery.replace_by_example(collection=self.test_1_col, example_data={ 'bla': 'xxx' }, new_value={
            'test': 'foo'
        })

        self.col1_doc2.retrieve()

        self.assertEqual(self.col1_doc2.test, 'foo')

    def test_remove_document(self):
        SimpleQuery.remove_by_example(collection=self.test_1_col, example_data={ 'bla': 'xxx' })

        all_docs = self.test_1_col.documents()

        self.assertEqual(len(all_docs), 1)

        doc = all_docs[0]
        self.assertDocumentsEqual(doc, self.col1_doc1)


class TraveserTestCase(ExtendedTestCase):
    def setUp(self):
        self.database_name = 'testcase_traverser_query_123'
        self.db = Database.create(name=self.database_name)

        # Create collections
        self.test_1_doc_col = self.db.create_collection('doc_col_1')
        self.test_1_edge_col = self.db.create_collection('edge_col_1', type=3)

        # Create test data
        self.doc1 = self.test_1_doc_col.create_document()
        self.doc1.ta='fa'
        self.doc1.save()

        self.doc2 = self.test_1_doc_col.create_document()
        self.doc2.ta='foo'
        self.doc2.save()

        # Create test relation
        self.edge1 = self.test_1_edge_col.create_edge(from_doc=self.doc1, to_doc=self.doc2, edge_data={
            'data': 'in_between'
        })

    def tearDown(self):
        # They need to be deleted
        Collection.remove(name=self.test_1_doc_col.name)
        Collection.remove(name=self.test_1_edge_col.name)

        Database.remove(name=self.database_name)

    def test_traverse_relation(self):
        result_list = Traveser.follow(
            start_vertex=self.doc1.id,
            edge_collection=self.test_1_edge_col.name,
            direction='outbound'
        )

        self.assertEqual(len(result_list), 1)

        result_doc = result_list[0]
        self.assertDocumentsEqual(result_doc, self.doc2)


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


class CollectionModelManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_collection_model_manager_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_retrieve_all_models(self):

        class TestModel(CollectionModel):
            pass

        TestModel.init()

        model1 = TestModel()
        model1.save()

        model2 = TestModel()
        model2.save()

        all_models = TestModel.objects.all()

        self.assertEqual(len(all_models), 2)

        TestModel.destroy()

    def test_iterate_over_queryset(self):

        class TestModel(CollectionModel):
            pass

        TestModel.init()

        model1 = TestModel()
        model1.save()

        model2 = TestModel()
        model2.save()

        all_models = TestModel.objects.all()

        for model in all_models:
            self.assertTrue(isinstance(model, TestModel))

        TestModel.destroy()



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


class CharFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equals(self):

        str1 = CharField()
        str1.set("jjj")

        str2 = CharField()
        str2.set("jjj")

        self.assertEqual(str1, str2)


class NumberFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_creation_with_default(self):
        number = 122
        field = NumberField(default=number)

        self.assertEqual(number, field.number)

    def test_equals(self):

        number1 = NumberField(null=False)
        number1.set(23)

        number2 = NumberField(null=False)
        number2.set(23)

        self.assertEqual(number1, number2)

    def test_wrong_input(self):

        number1 = NumberField()

        try:
            number1.set("ddd")
            self.assertTrue(False, msg='There should have been a NumberField.NotNullableFieldException')
        except:
            self.assertTrue(True)


class DateFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_creation_with_default(self):
        date = datetime.date.today()
        field = DateField(default=date)

        self.assertEqual(date, field.date)

    def test_equals(self):
        date = datetime.date.today()
        field1 = DateField()
        field1.set(date)

        field2 = DateField()
        field2.set(date)

        self.assertEqual(field1, field2)

    def test_not_equals(self):

        field1 = DateField(null=False)
        field2 = DateField(null=False)

        self.assertTrue(field1 != field2)


class DatetimeFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_creation_with_default(self):
        time = datetime.datetime.now()
        field = DatetimeField(default=time)

        self.assertEqual(time, field.time)

    def test_equals(self):
        time = datetime.datetime.now()

        field1 = DatetimeField()
        field1.set(time)

        field2 = DatetimeField()
        field2.set(time)

        self.assertEqual(field1, field2)

    def test_not_equals(self):

        field1 = DatetimeField(null=False)
        field2 = DatetimeField(null=False)

        self.assertTrue(field1 != field2)


class ForeignkeyFieldTestCase(unittest.TestCase):

    class TestModel(CollectionModel):
        collection_name = 'never_to_be_seen_again'

        test_field = CharField()

    def setUp(self):
        self.database_name = 'only_foreign_key_field_123'
        self.db = Database.create(name=self.database_name)

        ForeignkeyFieldTestCase.TestModel.init()

    def tearDown(self):
        ForeignkeyFieldTestCase.TestModel.destroy()

        Database.remove(name=self.database_name)

    def test_basic_creation_with_default(self):
        model = ForeignkeyFieldTestCase.TestModel()
        field = ForeignKeyField(to=CollectionModel, default=model)

        self.assertEqual(model, field.relation_model)

    def test_equals(self):
        model = ForeignkeyFieldTestCase.TestModel()

        field1 = ForeignKeyField(to=CollectionModel)
        field1.set(model)

        field2 = ForeignKeyField(to=CollectionModel)
        field2.set(model)

        self.assertEqual(field1, field2)


class TransactionTestCase(ExtendedTestCase):
    def setUp(self):

        self.database_name = 'testcase_transaction_123'
        self.db = Database.create(name=self.database_name)

        self.operating_collection = 'foo_test'
        self.test_1_col = Collection.create(name=self.operating_collection)

    def tearDown(self):
        Collection.remove(name=self.operating_collection)
        Database.remove(name=self.database_name)

    def test_create_document(self):

        trans = Transaction(collections={
            'write': [
                self.operating_collection,
            ]
        })

        # Uses already chosen database as usual
        collection = trans.collection(name=self.operating_collection)
        collection.create_document(data={
            'test': 'foo'
        })

        ctrl = TransactionController()

        transaction_result = ctrl.start(transaction=trans)

        transaction_doc = create_document_from_result_dict(transaction_result['result'], self.test_1_col.api)

        created_doc = SimpleQuery.get_by_example(self.test_1_col, example_data={
            '_id': transaction_doc.id
        })

        self.assertDocumentsEqual(transaction_doc, created_doc)

    def test_update_document(self):

        doc = self.test_1_col.create_document()
        doc.foo = 'bar'
        doc.save()

        trans = Transaction(collections={
            'write': [
                self.operating_collection,
            ]
        })

        new_foo_value = 'extra_bar'

        collection = trans.collection(self.operating_collection)
        collection.update_document(doc_id=doc.id, data={
            'foo': new_foo_value
        })

        ctrl = TransactionController()
        ctrl.start(transaction=trans)

        doc.retrieve()

        self.assertEqual(doc.foo, new_foo_value)


class IndexTestCase(ExtendedTestCase):
    def setUp(self):

        self.database_name = 'testcase_index_123'
        self.db = Database.create(name=self.database_name)

        self.operating_collection = 'foo_test'
        self.test_1_col = Collection.create(name=self.operating_collection)

    def tearDown(self):
        Collection.remove(name=self.operating_collection)
        Database.remove(name=self.database_name)


class UserTestCase(ExtendedTestCase):
    def setUp(self):

        self.database_name = 'testcase_user_123'
        self.db = Database.create(name=self.database_name)


    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_get_root(self):

        root = User.get(name='root')

        self.assertEqual(root.name, 'root')

    def test_create_and_delete_user_foo(self):

        user_name = 'foo'

        User.create(name=user_name, password='extra_key')

        foo_user = User.get(name=user_name)

        self.assertEqual(foo_user.name, user_name)

        User.remove(name=user_name)

if __name__ == '__main__':
    unittest.main()