import unittest
from arangodb.orm.fields import NumberField


class NumberFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_creation_with_default(self):
        number = 122
        field = NumberField(default=number)

        self.assertEqual(number, field.number)

    def test_equals(self):

        number1 = NumberField(null=False)
        number1.set(23)

        number2 = NumberField(null=False)
        number2.set(23)

        self.assertEqual(number1, number2)

    def test_wrong_input(self):

        number1 = NumberField()

        try:
            number1.set("ddd")
            self.assertTrue(False, msg='There should have been a NumberField.NotNullableFieldException')
        except:
            self.assertTrue(True)
