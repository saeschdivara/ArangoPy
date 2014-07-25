import unittest
from arangodb.api import Client, Database


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client(hostname='localhost')

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
        database_names = Database.get_all()

        self.assertTrue(len(database_names) >= 1)

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