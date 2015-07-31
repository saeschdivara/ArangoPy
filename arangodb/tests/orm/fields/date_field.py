import unittest
import datetime

from arangodb.orm.fields import DateField


class DateFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_creation_with_default(self):
        date = datetime.date.today()
        field = DateField(default=date)

        self.assertEqual(date, field.date)

    def test_equals(self):
        date = datetime.date.today()
        field1 = DateField()
        field1.set(date)

        field2 = DateField()
        field2.set(date)

        self.assertEqual(field1, field2)

    def test_not_equals(self):

        field1 = DateField(null=False)
        field1.set(datetime.date(2012, 12, 2))

        field2 = DateField(null=False)
        field2.set(datetime.date(2011, 11, 4))

        self.assertTrue(field1 != field2)
