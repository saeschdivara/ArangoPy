from arangodb.api import Database, Collection
from arangodb.index.api import Index
from arangodb.index.general import FulltextIndex
from arangodb.index.unique import HashIndex, GeoIndex, SkiplistIndex
from arangodb.query.simple import SimpleIndexQuery
from arangodb.tests.base import ExtendedTestCase


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