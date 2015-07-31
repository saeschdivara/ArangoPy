import unittest
from arangodb import six

from arangodb.orm.fields import UuidField


class UuidFieldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_state(self):

        uuid = UuidField()

        self.assertEqual(uuid.text, None)

        uuid.on_create(model_instance=None)

        self.assertTrue(isinstance(uuid.text, six.string_types))