import unittest
from uuid import uuid4
from arangodb.api import Database
from arangodb.orm.fields import NumberField, ForeignKeyField, BooleanField, CharField
from arangodb.orm.models import CollectionModel
from arangodb.query.advanced import Query


class CollectionModelManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_collection_model_manager_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_retrieve_one_specific_model_by_char(self):

        class TestModel(CollectionModel):
            uuid = CharField(null=False)

        TestModel.init()

        model1 = TestModel()
        model1.uuid = str(uuid4())
        model1.save()

        model2 = TestModel()
        model2.uuid = str(uuid4())
        model2.save()

        specific_model = TestModel.objects.get(uuid=model2.uuid)

        self.assertEqual(specific_model.uuid, model2.uuid)

        TestModel.destroy()

    def test_retrieve_one_specific_model_by_bool(self):

        class TestModel(CollectionModel):
            active = BooleanField(null=False)

        TestModel.init()

        model1 = TestModel()
        model1.active = False
        model1.save()

        model2 = TestModel()
        model2.active = True
        model2.save()

        specific_model1 = TestModel.objects.get(active=model1.active)
        specific_model2 = TestModel.objects.get(active=model2.active)

        self.assertEqual(specific_model1.document.id, model1.document.id)
        self.assertEqual(specific_model2.document.id, model2.document.id)

        TestModel.destroy()

    def test_queryset_clone(self):

        class TestModel(CollectionModel):
            active = BooleanField(null=False)

        TestModel.init()

        model1 = TestModel()
        model1.active = False
        model1.save()

        model2 = TestModel()
        model2.active = True
        model2.save()

        qs1 = TestModel.objects.all()

        self.assertEqual(len(qs1), 2)
        self.assertEqual(len(qs1._cache), 2)

        cloned_qs = qs1._clone()
        self.assertEqual(len(cloned_qs._cache), 0)

        TestModel.destroy()

    def test_retrieve_all_models(self):

        class TestModel(CollectionModel):
            pass

        TestModel.init()

        model1 = TestModel()
        model1.save()

        model2 = TestModel()
        model2.save()

        all_models = TestModel.objects.all()

        self.assertEqual(len(all_models), 2)

        TestModel.destroy()

    def test_filter_directly(self):

        class TestModel(CollectionModel):
            name = CharField()

        TestModel.init()

        model1 = TestModel()
        model1.name = 'test'
        model1.save()

        model2 = TestModel()
        model2.name = 'foo'
        model2.save()

        all_models = TestModel.objects.filter(name='foo')

        self.assertEqual(len(all_models), 1)

        model = all_models[0]

        self.assertEqual(model.id, model2.id)

        self.assertTrue(isinstance(model, TestModel))

        TestModel.destroy()

    def test_exclude_directly(self):

        class TestModel(CollectionModel):
            name = CharField()

        TestModel.init()

        model1 = TestModel()
        model1.name = 'test'
        model1.save()

        model2 = TestModel()
        model2.name = 'foo'
        model2.save()

        all_models = TestModel.objects.exclude(name='foo')

        self.assertEqual(len(all_models), 1)

        model = all_models[0]

        self.assertEqual(model.id, model1.id)

        self.assertTrue(isinstance(model, TestModel))

        TestModel.destroy()

    def test_iterate_over_queryset(self):

        class TestModel(CollectionModel):
            pass

        TestModel.init()

        model1 = TestModel()
        model1.save()

        model2 = TestModel()
        model2.save()

        all_models = TestModel.objects.all()

        for model in all_models:
            self.assertTrue(isinstance(model, TestModel))

        TestModel.destroy()

    def test_get_value_from_queryset_model(self):

        class TestModel(CollectionModel):

            text = CharField(null=False)

        TestModel.init()

        model1 = TestModel()
        model1.text = 'dd'
        model1.save()

        self.assertEqual(model1.text, 'dd')

        all_models = TestModel.objects.all()

        self.assertEqual(len(all_models), 1)

        model = all_models[0]
        self.assertEqual(model.text, 'dd')

        TestModel.destroy()

    def test_retrieve_all_models_and_update_one(self):

        class TestModel(CollectionModel):
            text = CharField(null=False)

        TestModel.init()

        model1 = TestModel()
        model1.text = 'aa'
        model1.save()

        model2 = TestModel()
        model2.text = 'aa'
        model2.save()

        all_models = TestModel.objects.all()

        self.assertEqual(len(all_models), 2)

        model = all_models[0]
        model.text = 'xx'
        model.save()

        all_models = TestModel.objects.all()

        self.assertEqual(len(all_models), 2)

        TestModel.destroy()

    def test_get_or_create_model(self):

        class TestModel(CollectionModel):
            active = BooleanField(null=False, default=False)

        TestModel.init()

        all_models = TestModel.objects.all()
        self.assertEqual(len(all_models), 0)

        model, is_created = TestModel.objects.get_or_create(active=True)

        self.assertEqual(is_created, True)
        self.assertEqual(model.active, True)

        model.save()

        model, is_created = TestModel.objects.get_or_create(active=True)

        self.assertEqual(is_created, False)
        self.assertEqual(model.active, True)

        all_models = TestModel.objects.all()
        self.assertEqual(len(all_models), 1)

        TestModel.destroy()

    def test_get_or_create_with_foreign_key_model(self):

        class ForeignTestModel(CollectionModel):
            active = BooleanField(null=False, default=False)

        class TestModel(CollectionModel):
            active = BooleanField(null=False, default=False)
            foreigner = ForeignKeyField(to=ForeignTestModel, related_name='other')

        ForeignTestModel.init()
        TestModel.init()

        normal_model = ForeignTestModel()
        normal_model.active = True
        normal_model.save()

        test_model, is_created = TestModel.objects.get_or_create(foreigner=normal_model)

        if is_created:
            test_model.save()

        TestModel.destroy()
        ForeignTestModel.destroy()

    def test_order_by_model_field_attribute_asc(self):

        class TestModel(CollectionModel):
            order = NumberField()

        TestModel.init()

        model1 = TestModel()
        model1.order = 3
        model1.save()

        model2 = TestModel()
        model2.order = 1
        model2.save()

        model3 = TestModel()
        model3.order = 2
        model3.save()

        all_models = TestModel.objects.all().order_by(field='order', order=Query.SORTING_ASC)

        self.assertEqual(len(all_models), 3)

        model = all_models[0]
        self.assertEqual(model.id, model2.id)

        model = all_models[1]
        self.assertEqual(model.id, model3.id)

        model = all_models[2]
        self.assertEqual(model.id, model1.id)

        TestModel.destroy()

    def test_order_by_model_field_attribute_desc(self):

        class TestModel(CollectionModel):
            order = NumberField()

        TestModel.init()

        model1 = TestModel()
        model1.order = 3
        model1.save()

        model2 = TestModel()
        model2.order = 1
        model2.save()

        model3 = TestModel()
        model3.order = 2
        model3.save()

        all_models = TestModel.objects.all().order_by(field='order', order=Query.SORTING_DESC)

        self.assertEqual(len(all_models), 3)

        model = all_models[0]
        self.assertEqual(model.id, model1.id)

        model = all_models[1]
        self.assertEqual(model.id, model3.id)

        model = all_models[2]
        self.assertEqual(model.id, model2.id)

        TestModel.destroy()

    def test_limit_model_list(self):

        class TestModel(CollectionModel):
            order = NumberField()

        TestModel.init()

        model1 = TestModel()
        model1.order = 3
        model1.save()

        model2 = TestModel()
        model2.order = 1
        model2.save()

        model3 = TestModel()
        model3.order = 2
        model3.save()

        all_models = TestModel.objects.limit(1).order_by(field='order', order=Query.SORTING_ASC)

        self.assertEqual(len(all_models), 1)

        model = all_models[0]
        self.assertEqual(model.id, model2.id)

        TestModel.destroy()

    def test_limit_with_start_model_list(self):

        class TestModel(CollectionModel):
            order = NumberField()

        TestModel.init()

        model1 = TestModel()
        model1.order = 3
        model1.save()

        model2 = TestModel()
        model2.order = 1
        model2.save()

        model3 = TestModel()
        model3.order = 2
        model3.save()

        all_models = TestModel.objects.all().order_by(field='order', order=Query.SORTING_ASC).limit(1, 1)

        self.assertEqual(len(all_models), 1)

        model = all_models[0]
        self.assertEqual(model.id, model3.id)

        TestModel.destroy()
