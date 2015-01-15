import unittest

from arangodb.api import Database
from arangodb.orm.fields import ForeignKeyField, CharField
from arangodb.orm.models import CollectionModel


class ForeignkeyFieldTestCase(unittest.TestCase):

    class TestModel(CollectionModel):
        collection_name = 'never_to_be_seen_again'

        test_field = CharField()

    def setUp(self):
        self.database_name = 'only_foreign_key_field_123'
        self.db = Database.create(name=self.database_name)

        ForeignkeyFieldTestCase.TestModel.init()

    def tearDown(self):
        ForeignkeyFieldTestCase.TestModel.destroy()

        Database.remove(name=self.database_name)

    def test_basic_creation_with_default(self):
        model = ForeignkeyFieldTestCase.TestModel()
        field = ForeignKeyField(to=CollectionModel, default=model)

        self.assertEqual(model, field.relation_model)

    def test_equals(self):
        model = ForeignkeyFieldTestCase.TestModel()

        field1 = ForeignKeyField(to=CollectionModel)
        field1.set(model)

        field2 = ForeignKeyField(to=CollectionModel)
        field2.set(model)

        self.assertEqual(field1, field2)

    def test_model_loading(self):

        model = ForeignkeyFieldTestCase.TestModel()

        field1 = ForeignKeyField(to=ForeignkeyFieldTestCase.TestModel)
        field1.loads(model)

        self.assertEqual(field1.relation_model, model)

    def test_other_side(self):

        class OtherModel(CollectionModel):
            my_side = ForeignKeyField(to=ForeignkeyFieldTestCase.TestModel, related_name='other_side')

        OtherModel.init()

        this_model = ForeignkeyFieldTestCase.TestModel()
        this_model.save()

        mo = OtherModel()
        mo.my_side = this_model
        mo.save()

        mo2 = OtherModel()
        mo2.my_side = this_model
        mo2.save()

        # print(this_model.other_side)

        self.assertEqual(len(this_model.other_side), 2)

        OtherModel.destroy()

    def test_other_side_filtering(self):

        class OtherModel(CollectionModel):
            my_side = ForeignKeyField(to=ForeignkeyFieldTestCase.TestModel, related_name='other_side')
            username = CharField()

        OtherModel.init()

        this_model = ForeignkeyFieldTestCase.TestModel()
        this_model.save()

        mo = OtherModel()
        mo.my_side = this_model
        mo.username = 'test'
        mo.save()

        mo2 = OtherModel()
        mo2.my_side = this_model
        mo2.username = 'not test'
        mo2.save()

        self.assertEqual(len(this_model.other_side), 2)

        filtered_other_side = this_model.other_side.filter(username='test')

        self.assertEqual(len(filtered_other_side), 1)

        filtered_model = filtered_other_side[0]

        self.assertEqual(filtered_model.id, mo.id)

        OtherModel.destroy()
