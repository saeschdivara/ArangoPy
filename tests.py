# Unit Tests
import unittest

# Test suites
from arangodb.tests import DatabaseTestCase, CollectionTestCase, AqlQueryTestCase



# Variables

test_suites = []
errors = 0
failures = 0

# Test suites
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DatabaseTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(AqlQueryTestCase) )

for test_suite in test_suites:

    # Tests runner
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)

    errors += len(result.errors)
    failures += len(result.failures)

import sys; sys.exit( errors + failures )