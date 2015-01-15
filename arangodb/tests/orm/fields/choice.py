import unittest
from arangodb.orm.fields import ChoiceField


class ChoiceFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_field_validation(self):

        choice = ChoiceField(choices=[
            ('value', 'DESCRIPTION'),
            ('value2', 'DESCRIPTION 2'),
        ])

        had_exception = False

        try:
            choice.set('not_valid_value')
        except Exception as err:
            had_exception = True


        self.assertTrue(had_exception, 'The value is not valid')

        choice.set('value2')
        self.assertTrue(True, 'The value is valid')

    def test_equals(self):

        choice1 = ChoiceField(choices=[
            ('value', 'DESCRIPTION'),
            ('value2', 'DESCRIPTION 2'),
        ])

        choice1.set('value')

        choice2 = ChoiceField(choices=[
            ('value', 'DESCRIPTION'),
            ('value2', 'DESCRIPTION 2'),
        ])

        choice2.set('value')

        self.assertEqual(choice1, choice2)

    def test_none_validation(self):

        choice = ChoiceField(choices=[
            ('value', 'DESCRIPTION'),
            ('value2', 'DESCRIPTION 2'),
        ], null=False)

        had_exception = False

        try:
            choice.validate()
        except:
            had_exception = True

        self.assertTrue(had_exception, 'The value cannot be None')