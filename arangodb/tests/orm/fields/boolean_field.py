import unittest

from arangodb.orm.fields import BooleanField


class BooleanFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_creation_with_default(self):
        boolean = False
        field = BooleanField(default=boolean)

        self.assertEqual(boolean, field.boolean)

    def test_equals(self):

        boolean1 = BooleanField()
        boolean1.set(True)

        boolean2 = BooleanField()
        boolean2.set(True)

        self.assertEqual(boolean1, boolean2)

        boolean1 = BooleanField()
        boolean1.set(False)

        boolean2 = BooleanField()
        boolean2.set(False)

        self.assertEqual(boolean1, boolean2)

    def test_equal_with_wrong_class(self):

        boolean1 = BooleanField()
        boolean1.set(False)

        self.assertTrue( not(boolean1 == False) )