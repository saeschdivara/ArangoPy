from arangodb.api import Database, Collection
from arangodb.query.advanced import Query
from arangodb.tests.base import ExtendedTestCase


class AqlEscapingTestCase(ExtendedTestCase):
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