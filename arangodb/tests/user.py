from arangodb.tests.base import ExtendedTestCase

from arangodb.api import Database
from arangodb.user import User


class UserTestCase(ExtendedTestCase):
    def setUp(self):

        self.database_name = 'testcase_user_123'
        self.db = Database.create(name=self.database_name)


    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_get_root(self):

        root = User.get(name='root')

        self.assertEqual(root.name, 'root')

    def test_create_and_delete_user_foo(self):

        user_name = 'foo'

        User.create(name=user_name, password='extra_key')

        foo_user = User.get(name=user_name)

        self.assertEqual(foo_user.name, user_name)

        User.remove(name=user_name)
