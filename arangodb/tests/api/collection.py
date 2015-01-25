import unittest

from arangodb.api import Database, Collection


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

    def test_different_document_revisions(self):

        collection_name = 'test_revision_documents'

        col = Collection.create(name=collection_name)
        doc1 = col.create_document()
        doc1.save()

        all_documents = col.documents()
        self.assertEqual(len(all_documents), 1)
        doc = all_documents[0]

        self.assertEqual(doc.revision, doc1.revision)

        doc.foo = 'bar'
        doc.save()

        self.assertNotEqual(doc.revision, doc1.revision)

        Collection.remove(name=collection_name)

    def test_remove_document_from_collection(self):

        collection_name = 'test_remove_document_from_collection'

        col = Collection.create(name=collection_name)
        doc1 = col.create_document()
        doc1.save()

        all_documents = col.documents()
        self.assertEqual(len(all_documents), 1)
        doc = all_documents[0]

        doc.delete()

        all_documents = col.documents()
        self.assertEqual(len(all_documents), 0)

        Collection.remove(name=collection_name)