# Unit Tests
import unittest

# Test suites
from .arangodb.tests.api.document import DocumentTestCase
from .arangodb.tests.api.collection import CollectionTestCase
from .arangodb.tests.api.database import DatabaseTestCase
from .arangodb.tests.endpoint import EndpointTestCase
from .arangodb.tests.index import IndexTestCase
from .arangodb.tests.orm.fields.boolean_field import BooleanFieldTestCase
from .arangodb.tests.orm.fields.char_field import CharFieldTestCase
from .arangodb.tests.orm.fields.choice import ChoiceFieldTestCase
from .arangodb.tests.orm.fields.date_field import DateFieldTestCase
from .arangodb.tests.orm.fields.datetime_field import DatetimeFieldTestCase
from .arangodb.tests.orm.fields.dict_field import DictFieldTestCase
from .arangodb.tests.orm.fields.foreignkey import ForeignkeyFieldTestCase
from .arangodb.tests.orm.fields.list_field import ListFieldTestCase
from .arangodb.tests.orm.fields.manytomany import ManyToManyFieldTestCase
from .arangodb.tests.orm.fields.number import NumberFieldTestCase
from .arangodb.tests.orm.fields.uuid_field import UuidFieldTestCase
from .arangodb.tests.orm.manager_with_index import CollectionModelManagerForIndexTestCase
from .arangodb.tests.orm.model import CollectionModelTestCase
from .arangodb.tests.orm.model_foreignkey import CollectionModelForeignKeyFieldTestCase
from .arangodb.tests.orm.model_manager import CollectionModelManagerTestCase
from .arangodb.tests.query.advanced import TraveserTestCase
from .arangodb.tests.query.aql import AqlQueryTestCase
from .arangodb.tests.query.basic import SimpleQueryTestCase
from .arangodb.tests.query.index import SimpleIndexQueryTestCase
from .arangodb.tests.transaction import TransactionTestCase
from .arangodb.tests.user import UserTestCase


# Variables

test_suites = []
errors = 0
failures = 0

# Test suites
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DatabaseTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DocumentTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(AqlQueryTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(SimpleQueryTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(SimpleIndexQueryTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(TraveserTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelManagerTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelManagerForIndexTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelForeignKeyFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(ListFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DictFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(BooleanFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CharFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(UuidFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(ChoiceFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(NumberFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DateFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DatetimeFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(ForeignkeyFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(ManyToManyFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(TransactionTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(IndexTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(UserTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(EndpointTestCase) )

for test_suite in test_suites:

    # Tests runner
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)

    errors += len(result.errors)
    failures += len(result.failures)

import sys; sys.exit( errors + failures )