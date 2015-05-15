import unittest

from arangodb.tests.api.document import DocumentTestCase
from arangodb.tests.api.collection import CollectionTestCase
from arangodb.tests.api.database import DatabaseTestCase
from arangodb.tests.endpoint import EndpointTestCase
from arangodb.tests.index import IndexTestCase
from arangodb.tests.orm.fields.boolean_field import BooleanFieldTestCase
from arangodb.tests.orm.fields.char_field import CharFieldTestCase
from arangodb.tests.orm.fields.choice import ChoiceFieldTestCase
from arangodb.tests.orm.fields.date_field import DateFieldTestCase
from arangodb.tests.orm.fields.datetime_field import DatetimeFieldTestCase
from arangodb.tests.orm.fields.dict_field import DictFieldTestCase
from arangodb.tests.orm.fields.foreignkey import ForeignkeyFieldTestCase
from arangodb.tests.orm.fields.list_field import ListFieldTestCase
from arangodb.tests.orm.fields.manytomany import ManyToManyFieldTestCase
from arangodb.tests.orm.fields.number import NumberFieldTestCase
from arangodb.tests.orm.fields.uuid_field import UuidFieldTestCase
from arangodb.tests.orm.manager_with_index import CollectionModelManagerForIndexTestCase
from arangodb.tests.orm.model import CollectionModelTestCase
from arangodb.tests.orm.model_foreignkey import CollectionModelForeignKeyFieldTestCase
from arangodb.tests.orm.model_manager import CollectionModelManagerTestCase
from arangodb.tests.query.advanced import TraveserTestCase
from arangodb.tests.query.aql import AqlQueryTestCase
from arangodb.tests.query.basic import SimpleQueryTestCase
from arangodb.tests.query.escaping import AqlEscapingTestCase
from arangodb.tests.query.index import SimpleIndexQueryTestCase
from arangodb.tests.transaction import TransactionTestCase
from arangodb.tests.user import UserTestCase


if __name__ == '__main__':
    unittest.main()