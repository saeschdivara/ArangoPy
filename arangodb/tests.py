import unittest
from arangodb.api import Client, Database, Collection


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

class AqlQueryTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_this(self):  ## test method names begin 'test*'
        self.assertEqual((1 + 2), 3)
        self.assertEqual(0 + 1, 1)

    def testMultiply(self):
        self.assertEqual((0 * 10), 0)
        self.assertEqual((5 * 8), 40)

if __name__ == '__main__':
    unittest.main()