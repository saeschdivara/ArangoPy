from arangodb.tests.base import ExtendedTestCase

from arangodb.api import Database, Collection
from arangodb.query.simple import SimpleQuery
from arangodb.query.utils.document import create_document_from_result_dict
from arangodb.transaction.controller import TransactionController, Transaction


class TransactionTestCase(ExtendedTestCase):
    def setUp(self):

        self.database_name = 'testcase_transaction_123'
        self.db = Database.create(name=self.database_name)

        self.operating_collection = 'foo_test'
        self.test_1_col = Collection.create(name=self.operating_collection)

    def tearDown(self):
        Collection.remove(name=self.operating_collection)
        Database.remove(name=self.database_name)

    def test_create_document(self):

        trans = Transaction(collections={
            'write': [
                self.operating_collection,
            ]
        })

        # Uses already chosen database as usual
        collection = trans.collection(name=self.operating_collection)
        collection.create_document(data={
            'test': 'foo'
        })

        ctrl = TransactionController()

        transaction_result = ctrl.start(transaction=trans)

        transaction_doc = create_document_from_result_dict(transaction_result['result'], self.test_1_col.api)

        created_doc = SimpleQuery.get_by_example(self.test_1_col, example_data={
            '_id': transaction_doc.id
        })

        self.assertDocumentsEqual(transaction_doc, created_doc)

    def test_update_document(self):

        doc = self.test_1_col.create_document()
        doc.foo = 'bar'
        doc.save()

        trans = Transaction(collections={
            'write': [
                self.operating_collection,
            ]
        })

        new_foo_value = 'extra_bar'

        collection = trans.collection(self.operating_collection)
        collection.update_document(doc_id=doc.id, data={
            'foo': new_foo_value
        })

        ctrl = TransactionController()
        ctrl.start(transaction=trans)

        doc.retrieve()

        self.assertEqual(doc.foo, new_foo_value)