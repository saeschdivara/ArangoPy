import unittest
from arangodb.api import Database, Collection
from arangodb.orm.fields import CharField, ManyToManyField
from arangodb.orm.models import CollectionModel


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