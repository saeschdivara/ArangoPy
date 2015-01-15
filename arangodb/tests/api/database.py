import unittest

from arangodb.api import Database


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