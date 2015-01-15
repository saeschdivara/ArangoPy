from arangodb.tests.base import ExtendedTestCase

from arangodb.api import Collection, Database
from arangodb.index.api import Index
from arangodb.index.general import CapConstraintIndex, FulltextIndex
from arangodb.index.unique import HashIndex, GeoIndex, SkiplistIndex


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