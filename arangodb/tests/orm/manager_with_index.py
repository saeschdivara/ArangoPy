import unittest

from arangodb.api import Database
from arangodb.index.general import FulltextIndex
from arangodb.index.unique import GeoIndex, SkiplistIndex, HashIndex
from arangodb.orm.fields import NumberField, TextField, CharField
from arangodb.orm.models import CollectionModel


class CollectionModelManagerForIndexTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_collection_model_manager_for_index_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_search_for_hash_index_on_field(self):

        class TestModel(CollectionModel):

            username_index = HashIndex(fields=['username'])
            username = CharField(required=True, null=False)

        TestModel.init()

        model1 = TestModel()
        model1.username = 'test_user_1'
        model1.save()

        model2 = TestModel()
        model2.username = 'test_user_2'
        model2.save()

        models = TestModel.objects.search_by_index(index='username_index', username='test_user_2')

        self.assertEqual(len(models), 1)

        model = models[0]
        self.assertEqual(model.id, model2.id)

        TestModel.destroy()

    def test_search_for_skiplist_index_on_field(self):

        class TestModel(CollectionModel):

            username_index = SkiplistIndex(fields=['username'])
            username = CharField(required=True, null=False)

        TestModel.init()

        model1 = TestModel()
        model1.username = 'test_user_1'
        model1.save()

        model2 = TestModel()
        model2.username = 'test_user_2'
        model2.save()

        models = TestModel.objects.search_by_index(index='username_index', username='test_user_2')

        self.assertEqual(len(models), 1)

        model = models[0]
        self.assertEqual(model.id, model2.id)

        TestModel.destroy()

    def test_search_for_skiplist_range_index_on_field(self):

        class TestModel(CollectionModel):

            rank_index = SkiplistIndex(fields=['rank'])
            rank = NumberField(required=True, null=False)

        TestModel.init()

        model1 = TestModel()
        model1.rank = 3
        model1.save()

        model2 = TestModel()
        model2.rank = 5
        model2.save()

        model3 = TestModel()
        model3.rank = 4
        model3.save()

        model4 = TestModel()
        model4.rank = 7
        model4.save()

        models = TestModel.objects.search_in_range(
            index='rank_index',
            attribute='rank',
            left=5,
            right=8,
            closed=True,
        )

        self.assertEqual(len(models), 2)

        model_id_pool = ( model2.id, model4.id, )

        result_model_1 = models[0]
        result_model_2 = models[1]

        self.assertTrue( result_model_1.id in model_id_pool )
        self.assertTrue( result_model_2.id in model_id_pool )

        self.assertNotEqual( result_model_1.id, result_model_2.id )

        TestModel.destroy()


    def test_search_fulltext_index_on_field(self):

        class TestModel(CollectionModel):

            description_index = FulltextIndex(fields=['description'], minimum_length=5)
            description = TextField(required=True, null=False)

        TestModel.init()

        model1 = TestModel()
        model1.description = "I want to really parse this description."
        model1.save()

        model2 = TestModel()
        model2.description = "Really, do I need to parse this description thing."
        model2.save()

        model3 = TestModel()
        model3.description = "What is that crappy thing?"
        model3.save()

        # Show that the words can be upper or lower case
        result = TestModel.objects.search_fulltext(
            index='description_index',
            attribute='description',
            example_text='really'
        )

        self.assertEqual(len(result), 2)

        # Show that . is ignored
        result = TestModel.objects.search_fulltext(
            index='description_index',
            attribute='description',
            example_text='description'
        )

        self.assertEqual(len(result), 2)

        # There cannot always be found 2
        result = TestModel.objects.search_fulltext(
            index='description_index',
            attribute='description',
            example_text='crappy'
        )

        self.assertEqual(len(result), 1)

        TestModel.destroy()

    def test_search_geo_near_index(self):

        class TestModel(CollectionModel):

            position_index = GeoIndex(fields=['latitude', 'longitude'], geo_json=False)
            latitude = NumberField(required=True, null=False)
            longitude = NumberField(required=True, null=False)

        TestModel.init()

        # Paris
        model1 = TestModel()
        model1.latitude = 48.853333
        model1.longitude = 2.348611
        model1.save()

        # Koeln
        model2 = TestModel()
        model2.latitude = 50.933333
        model2.longitude = 6.95
        model2.save()

        # Brussels
        models = TestModel.objects.search_near(
            index='position_index',
            latitude=50.850278,
            longitude=4.348611,
            limit=1,
        )

        self.assertEqual(len(models), 1)

        model = models[0]
        self.assertEqual(model.id, model2.id)

        TestModel.destroy()

    def test_search_geo_within_index(self):

        class TestModel(CollectionModel):

            position_index = GeoIndex(fields=['latitude', 'longitude'], geo_json=False)
            latitude = NumberField(required=True, null=False)
            longitude = NumberField(required=True, null=False)

        TestModel.init()

        # Paris
        model1 = TestModel()
        model1.latitude = 48.853333
        model1.longitude = 2.348611
        model1.save()

        # Koeln
        model2 = TestModel()
        model2.latitude = 50.933333
        model2.longitude = 6.95
        model2.save()

        radius_kilometers = 400
        radius_meters = radius_kilometers * 1000

        # Brussels
        models = TestModel.objects.search_within(
            index='position_index',
            latitude=50.850278,
            longitude=4.348611,
            radius=radius_meters,
            limit=1,
        )

        self.assertEqual(len(models), 1)

        model = models[0]
        self.assertEqual(model.id, model2.id)

        TestModel.destroy()