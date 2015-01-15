import unittest
import datetime

from arangodb.orm.fields import DatetimeField


class DatetimeFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_creation_with_default(self):
        time = datetime.datetime.now()
        field = DatetimeField(default=time)

        self.assertEqual(time, field.time)

    def test_equals(self):
        time = datetime.datetime.now()

        field1 = DatetimeField()
        field1.set(time)

        field2 = DatetimeField()
        field2.set(time)

        self.assertEqual(field1, field2)

    def test_not_equals(self):

        field1 = DatetimeField(null=False)
        field2 = DatetimeField(null=False)

        self.assertTrue(field1 != field2)