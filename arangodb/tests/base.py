import unittest

from arangodb.api import Client


class ExtendedTestCase(unittest.TestCase):
    def assertDocumentsEqual(self, doc1, doc2):
        """
        """

        self.assertEqual(doc1.id, doc2.id)

        for prop in doc1.data:
            doc1_val = doc1.data[prop]
            doc2_val = doc2.data[prop]

            self.assertEqual(doc1_val, doc2_val)



client = Client(hostname='localhost', auth=('root', ''))