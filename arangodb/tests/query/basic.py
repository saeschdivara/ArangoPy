from arangodb.api import Database, Collection
from arangodb.query.simple import SimpleQuery
from arangodb.tests.base import ExtendedTestCase


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