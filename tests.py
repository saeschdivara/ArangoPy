# Unit Tests
import unittest

# Test suites
from arangodb.tests import DatabaseTestCase, CollectionTestCase, AqlQueryTestCase, DocumentTestCase, SimpleQueryTestCase, \
    CollectionModelTestCase, CollectionModelForeignKeyFieldTestCase, TraveserTestCase, TransactionTestCase, \
    CharFieldTestCase, NumberFieldTestCase, DateFieldTestCase, DatetimeFieldTestCase


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
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(TraveserTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelForeignKeyFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CharFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(NumberFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DateFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DatetimeFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(TransactionTestCase) )

for test_suite in test_suites:

    # Tests runner
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)

    errors += len(result.errors)
    failures += len(result.failures)

import sys; sys.exit( errors + failures )