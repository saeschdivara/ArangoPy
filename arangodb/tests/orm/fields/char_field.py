import unittest
from arangodb.orm.fields import CharField


class CharFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equals(self):

        str1 = CharField()
        str1.set("jjj")

        str2 = CharField()
        str2.set("jjj")

        self.assertEqual(str1, str2)