import unittest
from arangodb.api import Document
from arangodb.tests.base import client


class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_document_access_values_by_attribute_getter(self):
        doc = Document(id='', key='', collection='', api=client.api)
        # set this to true so it won't make requests to nothing
        doc.is_loaded = True
        doc_attr_value = 'foo_bar'
        doc.set(key='test', value=doc_attr_value)

        self.assertEqual(doc.test, doc_attr_value)

    def test_document_access_values_by_attribute_setter(self):
        doc = Document(id='', key='', collection='', api=client.api)
        # set this to true so it won't make requests to nothing
        doc.is_loaded = True
        doc_attr_value = 'foo_bar'

        doc.test = doc_attr_value

        self.assertEqual(doc.get(key='test'), doc_attr_value)