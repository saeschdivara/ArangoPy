import unittest
import datetime
from uuid import uuid4

from arangodb.api import Client, Database, Collection, Document
from arangodb.index.api import Index
from arangodb.index.general import FulltextIndex, CapConstraintIndex
from arangodb.index.unique import HashIndex, SkiplistIndex, GeoIndex
from arangodb.orm.fields import CharField, ForeignKeyField, NumberField, DatetimeField, DateField, BooleanField, \
    UuidField, ManyToManyField, ChoiceField
from arangodb.orm.models import CollectionModel
from arangodb.query.advanced import Query, Traveser
from arangodb.query.utils.document import create_document_from_result_dict
from arangodb.query.simple import SimpleQuery, SimpleIndexQuery
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

    def test_getting_new_info_for_collection(self):

        collection_name = 'test_foo_123'

        col = Collection.create(name=collection_name)

        retrieved_col = Collection.get_loaded_collection(name=collection_name)
        retrieved_col.set_data(waitForSync=True)
        retrieved_col.save()

        col.get()

        self.assertEqual(col.waitForSync, True)

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


class SimpleIndexQueryTestCase(ExtendedTestCase):
    def setUp(self):
        self.database_name = 'testcase_simple_index_query_123'
        self.db = Database.create(name=self.database_name)

        # Create test data
        self.test_1_col = self.db.create_collection('foo_1')

        self.hash_index = Index(self.test_1_col, HashIndex(fields=[
            'username'
        ]))

        self.geo_index = Index(self.test_1_col, GeoIndex(fields=['latitude', 'longitude'], geo_json=False))

        self.fulltext_index = Index(self.test_1_col, FulltextIndex(fields=['description'], minimum_length=4))

        self.skiplist_index = Index(self.test_1_col, SkiplistIndex(fields=['rated'], unique=False))

        self.hash_index.save()
        self.geo_index.save()
        self.fulltext_index.save()
        self.skiplist_index.save()

        self.col1_doc1 = self.test_1_col.create_document()
        self.col1_doc1.username='surgent'
        self.col1_doc1.description='Paris is such a beautiful city'
        self.col1_doc1.city= 'Paris'
        self.col1_doc1.latitude= 48.853333
        self.col1_doc1.longitude= 2.348611
        self.col1_doc1.rated= 4
        self.col1_doc1.save()

        self.col1_doc2 = self.test_1_col.create_document()
        self.col1_doc2.username='name killer'
        self.col1_doc2.description='The next time I will get myself some tickets for this event'
        self.col1_doc2.city='Koeln'
        self.col1_doc2.latitude= 50.933333
        self.col1_doc2.longitude=6.95
        self.col1_doc2.rated= 4
        self.col1_doc2.save()

        self.col1_doc3 = self.test_1_col.create_document()
        self.col1_doc3.username='fa boor'
        self.col1_doc3.description='I have never seen such a big door in a city'
        self.col1_doc3.city='Berlin'
        self.col1_doc3.latitude=52.524167
        self.col1_doc3.longitude=13.410278
        self.col1_doc3.rated= 8
        self.col1_doc3.save()

        self.col1_doc4 = self.test_1_col.create_document()
        self.col1_doc4.username='haba'
        self.col1_doc4.description='It one of the best cities in the world'
        self.col1_doc4.city='Rome'
        self.col1_doc4.latitude=41.891667
        self.col1_doc4.longitude=12.511111
        self.col1_doc4.rated= 10
        self.col1_doc4.save()

    def tearDown(self):
        # Delete index
        self.geo_index.delete()
        self.hash_index.delete()
        self.fulltext_index.delete()
        self.skiplist_index.delete()

        # They need to be deleted
        Collection.remove(name=self.test_1_col.name)

        Database.remove(name=self.database_name)

    def test_get_only_by_hash_index(self):
        """
        """

        doc1 = SimpleIndexQuery.get_by_example_hash(collection=self.test_1_col,
                                                    index_id=self.hash_index.index_type_obj.id,
                                                    example_data={
            'username': self.col1_doc1.username
        })

        self.assertDocumentsEqual(doc1, self.col1_doc1)

    def test_within_position(self):
        """
        """

        # 52.370278, 9.733056 => Hannover (Germany)

        radius_kilometers = 400
        radius_meters = radius_kilometers * 1000

        in_radius_docs = SimpleIndexQuery.within(
            collection=self.test_1_col,
            latitude= 52.370278,
            longitude=9.733056,
            radius=radius_meters,
            index_id=self.geo_index.index_type_obj.id
        )

        self.assertEqual(len(in_radius_docs), 2)

        koeln_doc = in_radius_docs[0]
        berlin_doc = in_radius_docs[1]

        self.assertDocumentsEqual(koeln_doc, self.col1_doc2)
        self.assertDocumentsEqual(berlin_doc, self.col1_doc3)


    def test_near_position(self):
        """
        """

        # 50.850278, 4.348611 => Brussels

        near_docs = SimpleIndexQuery.near(
            collection=self.test_1_col,
            latitude=50.850278,
            longitude=4.348611,
            index_id=self.geo_index.index_type_obj.id,
            limit=2
        )

        self.assertEqual(len(near_docs), 2)

        koeln_doc = near_docs[0]
        paris_doc = near_docs[1]

        self.assertDocumentsEqual(koeln_doc, self.col1_doc2)
        self.assertDocumentsEqual(paris_doc, self.col1_doc1)

    def test_fulltext_search(self):
        """
        """

        docs_with_description = SimpleIndexQuery.fulltext(
            collection=self.test_1_col,
            attribute='description',
            example_text='city',
            index_id=self.fulltext_index.index_type_obj.id
        )

        self.assertNotEqual(docs_with_description, None)
        self.assertEqual(len(docs_with_description), 2)


        paris_doc = docs_with_description[0]
        berlin_doc = docs_with_description[1]

        self.assertDocumentsEqual(paris_doc, self.col1_doc1)
        self.assertDocumentsEqual(berlin_doc, self.col1_doc3)

    def test_skiplist_by_example(self):
        """
        """

        docs_with_rating = SimpleIndexQuery.get_by_example_skiplist(
            collection=self.test_1_col,
            index_id=self.skiplist_index.index_type_obj.id,
            example_data={ 'rated': 4 }
        )

        self.assertNotEqual(docs_with_rating, None)
        self.assertEqual(len(docs_with_rating), 2)


        paris_doc = docs_with_rating[0]
        koeln_doc = docs_with_rating[1]

        self.assertDocumentsEqual(paris_doc, self.col1_doc1)
        self.assertDocumentsEqual(koeln_doc, self.col1_doc2)

    def test_skiplist_range(self):
        """
        """

        docs_with_rating = SimpleIndexQuery.range(
            collection=self.test_1_col,
            attribute='rated',
            left=8,
            right=10,
            closed=True,
            index_id=self.skiplist_index.index_type_obj.id,
        )

        self.assertNotEqual(docs_with_rating, None)
        self.assertEqual(len(docs_with_rating), 2)

        berlin_doc = docs_with_rating[0]
        rome_doc = docs_with_rating[1]

        self.assertDocumentsEqual(berlin_doc, self.col1_doc3)
        self.assertDocumentsEqual(rome_doc, self.col1_doc4)


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


class CollectionModelManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_collection_model_manager_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_retrieve_one_specific_model_by_char(self):

        class TestModel(CollectionModel):
            uuid = CharField(null=False)

        TestModel.init()

        model1 = TestModel()
        model1.uuid = str(uuid4())
        model1.save()

        model2 = TestModel()
        model2.uuid = str(uuid4())
        model2.save()

        specific_model = TestModel.objects.get(uuid=model2.uuid)

        self.assertEqual(specific_model.uuid, model2.uuid)

        TestModel.destroy()

    def test_retrieve_one_specific_model_by_bool(self):

        class TestModel(CollectionModel):
            active = BooleanField(null=False)

        TestModel.init()

        model1 = TestModel()
        model1.active = False
        model1.save()

        model2 = TestModel()
        model2.active = True
        model2.save()

        specific_model1 = TestModel.objects.get(active=model1.active)
        specific_model2 = TestModel.objects.get(active=model2.active)

        self.assertEqual(specific_model1.document.id, model1.document.id)
        self.assertEqual(specific_model2.document.id, model2.document.id)

        TestModel.destroy()

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

    def test_get_value_from_queryset_model(self):

        class TestModel(CollectionModel):

            text = CharField(null=False)

        TestModel.init()

        model1 = TestModel()
        model1.text = 'dd'
        model1.save()

        self.assertEqual(model1.text, 'dd')

        all_models = TestModel.objects.all()

        self.assertEqual(len(all_models), 1)

        model = all_models[0]
        self.assertEqual(model.text, 'dd')

        TestModel.destroy()

    def test_retrieve_all_models_and_update_one(self):

        class TestModel(CollectionModel):
            text = CharField(null=False)

        TestModel.init()

        model1 = TestModel()
        model1.text = 'aa'
        model1.save()

        model2 = TestModel()
        model2.text = 'aa'
        model2.save()

        all_models = TestModel.objects.all()

        self.assertEqual(len(all_models), 2)

        model = all_models[0]
        model.text = 'xx'
        model.save()

        all_models = TestModel.objects.all()

        self.assertEqual(len(all_models), 2)

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


class BooleanFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_creation_with_default(self):
        boolean = False
        field = BooleanField(default=boolean)

        self.assertEqual(boolean, field.boolean)

    def test_equals(self):

        boolean1 = BooleanField()
        boolean1.set(True)

        boolean2 = BooleanField()
        boolean2.set(True)

        self.assertEqual(boolean1, boolean2)

        boolean1 = BooleanField()
        boolean1.set(False)

        boolean2 = BooleanField()
        boolean2.set(False)

        self.assertEqual(boolean1, boolean2)

    def test_equal_with_wrong_class(self):

        boolean1 = BooleanField()
        boolean1.set(False)

        self.assertTrue( not(boolean1 == False) )


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


class UuidFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_state(self):

        uuid = UuidField()

        self.assertEqual(uuid.text, None)

        uuid.on_create(model_instance=None)

        self.assertTrue(isinstance(uuid.text, basestring))


class ChoiceFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_field_validation(self):

        choice = ChoiceField(choices=[
            ('DESCRIPTION', 'value'),
            ('DESCRIPTION 2', 'value2'),
        ])

        had_exception = False

        try:
            choice.set('not_valid_value')
        except Exception as err:
            had_exception = True


        self.assertTrue(had_exception, 'The value is not valid')

        choice.set('value2')
        self.assertTrue(True, 'The value is valid')

    def test_equals(self):

        choice1 = ChoiceField(choices=[
            ('DESCRIPTION', 'value'),
            ('DESCRIPTION 2', 'value2'),
        ])

        choice1.set('value')

        choice2 = ChoiceField(choices=[
            ('DESCRIPTION', 'value'),
            ('DESCRIPTION 2', 'value2'),
        ])

        choice2.set('value')

        self.assertEqual(choice1, choice2)

    def test_none_validation(self):

        choice = ChoiceField(choices=[
            ('DESCRIPTION', 'value'),
            ('DESCRIPTION 2', 'value2'),
        ], null=False)

        had_exception = False

        try:
            choice.validate()
        except:
            had_exception = True

        self.assertTrue(had_exception, 'The value cannot be None')


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


class ManyToManyFieldTestCase(unittest.TestCase):

    def setUp(self):
        self.database_name = 'only_many_to_many_field_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_basic_creation_with_default(self):


        class EndModel(CollectionModel):

            test_field = CharField()


        class StartModel(CollectionModel):
            collection_name = 'never_to_be_seen_again'

            others = ManyToManyField(to=EndModel, related_name='starters')

        EndModel.init()
        StartModel.init()

        end_model1 = EndModel()
        end_model1.test_field = 'foo'
        end_model1.save()

        end_model2 = EndModel()
        end_model2.test_field = 'bar'
        end_model2.save()

        start_model = StartModel()
        start_model.others = [end_model1, end_model2]
        start_model.save()

        relation_collection_name = start_model.get_field(name='others')._get_relation_collection_name(StartModel)
        col = Collection.get_loaded_collection(name=relation_collection_name)
        relation_documents = col.documents()

        self.assertEqual(len(relation_documents), 2)

        rel1 = relation_documents[0]
        rel2 = relation_documents[1]

        # From is always the same
        self.assertEqual(rel1._from, start_model.document.id)
        self.assertEqual(rel2._from, start_model.document.id)

        is_first_the_first_end_model = rel1._to == end_model1.document.id
        is_first_the_second_end_model = rel1._to == end_model2.document.id
        self.assertTrue(is_first_the_first_end_model or is_first_the_second_end_model)

        is_second_the_first_end_model = rel2._to == end_model1.document.id
        is_second_the_second_end_model = rel2._to == end_model2.document.id
        self.assertTrue(is_second_the_first_end_model or is_second_the_second_end_model)

        StartModel.destroy()
        EndModel.destroy()

    def test_getting_related_objects(self):


        class EndModel(CollectionModel):

            test_field = CharField()


        class StartModel(CollectionModel):
            collection_name = 'never_to_be_seen_again'

            others = ManyToManyField(to=EndModel, related_name='starters')

        EndModel.init()
        StartModel.init()

        end_model1 = EndModel()
        end_model1.test_field = 'foo'
        end_model1.save()

        end_model2 = EndModel()
        end_model2.test_field = 'bar'
        end_model2.save()

        end_model3 = EndModel()
        end_model3.test_field = 'extra'
        end_model3.save()

        start_model = StartModel()
        start_model.others = [end_model1, end_model2]
        start_model.save()

        start_model = StartModel.objects.get(_id=start_model.document.id)

        related_models = start_model.others

        self.assertEqual(len(related_models), 2)

        rel1 = related_models[0]
        rel2 = related_models[1]

        is_first_the_first_end_model = rel1.document.id == end_model1.document.id
        is_first_the_second_end_model = rel1.document.id == end_model2.document.id
        self.assertTrue(is_first_the_first_end_model or is_first_the_second_end_model)

        is_second_the_first_end_model = rel2.document.id == end_model1.document.id
        is_second_the_second_end_model = rel2.document.id == end_model2.document.id
        self.assertTrue(is_second_the_first_end_model or is_second_the_second_end_model)

        # Test if the end model can retrieve the starter model
        self.assertEqual(len(end_model1.starters), 1)

        starter = end_model1.starters[0]
        self.assertEqual(starter.document.id, start_model.document.id)

        StartModel.destroy()
        EndModel.destroy()


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

        self.database_name = 'testcase_index_222_123'
        self.db = Database.create(name=self.database_name)

        self.operating_collection = 'bar_extra'
        self.test_1_col = Collection.create(name=self.operating_collection)

    def tearDown(self):
        Collection.remove(name=self.operating_collection)
        Database.remove(name=self.database_name)

    def test_unique_hash_index(self):

        index = Index(self.test_1_col, HashIndex(fields=[
            'username'
        ]))

        index.save()

        index.delete()

    def test_unique_skiptlist_index(self):

        index = Index(self.test_1_col, SkiplistIndex(fields=[
            'username'
        ]))

        index.save()

        index.delete()

    def test_unique_geo_index(self):

        index = Index(self.test_1_col, GeoIndex(fields=[
            'position'
        ], geo_json=True
        ))

        index.save()

        index.delete()

    def test_fulltext_index(self):

        index = Index(self.test_1_col, FulltextIndex(fields=[
            'description'
        ], minimum_length=5))

        index.save()

        index.delete()

    def test_cap_constraint_index(self):

        index = Index(self.test_1_col, CapConstraintIndex(size=5))

        index.save()

        index.delete()

    def test_overwrite_index_definition(self):

        index = Index(self.test_1_col, HashIndex(fields=[
            'username'
        ]))

        index.save()

        doc1 = self.test_1_col.create_document()
        doc1.username = 'test'
        doc1.save()

        has_exception = False

        doc2 = self.test_1_col.create_document()
        doc2.username = 'test'

        try:
            doc2.save()
        except:
            has_exception = True

        self.assertTrue(has_exception)

        index.index_type_obj.unique = False

        index.overwrite()

        has_exception = False

        try:
            doc2.save()
        except:
            has_exception = True

        self.assertFalse(has_exception)

        index.delete()


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