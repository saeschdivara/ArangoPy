from arangodb.api import Collection, Database
from arangodb.query.advanced import Traveser
from arangodb.tests.base import ExtendedTestCase


class TraveserTestCase(ExtendedTestCase):
    def setUp(self):
        self.database_name = 'testcase_traverser_query_123'
        self.db = Database.create(name=self.database_name)

        # Create collections
        self.test_1_doc_col = self.db.create_collection('doc_col_1')
        self.test_1_edge_col = self.db.create_collection('edge_col_1', type=3)

        # Create test data
        self.doc1 = self.test_1_doc_col.create_document()
        self.doc1.ta='fa'
        self.doc1.save()

        self.doc2 = self.test_1_doc_col.create_document()
        self.doc2.ta='foo'
        self.doc2.save()

        self.doc3 = self.test_1_doc_col.create_document()
        self.doc3.ta='bar'
        self.doc3.save()

        self.doc4 = self.test_1_doc_col.create_document()
        self.doc4.ta='extra'
        self.doc4.save()

        # Create test relation
        self.edge1 = self.test_1_edge_col.create_edge(from_doc=self.doc1, to_doc=self.doc2, edge_data={
            'data': 'in_between'
        })

        self.edge2 = self.test_1_edge_col.create_edge(from_doc=self.doc1, to_doc=self.doc3, edge_data={
            'data': 'xxx'
        })

        self.edge3 = self.test_1_edge_col.create_edge(from_doc=self.doc1, to_doc=self.doc4, edge_data={
            'data': 'dd'
        })

        self.edge4 = self.test_1_edge_col.create_edge(from_doc=self.doc2, to_doc=self.doc4, edge_data={
            'data': 'aa'
        })

    def tearDown(self):
        # They need to be deleted
        Collection.remove(name=self.test_1_doc_col.name)
        Collection.remove(name=self.test_1_edge_col.name)

        Database.remove(name=self.database_name)

    def test_traverse_relation(self):
        result_list = Traveser.follow(
            start_vertex=self.doc1.id,
            edge_collection=self.test_1_edge_col.name,
            direction='outbound'
        )

        # 1 -> 2 -> 4
        # 1 -> 4
        # 1 -> 3
        self.assertEqual(len(result_list), 4)

        result_doc1 = result_list[0]
        self.assertDocumentsEqual(result_doc1, self.doc2)

        result_doc2 = result_list[1]
        self.assertDocumentsEqual(result_doc2, self.doc4)

        result_doc3 = result_list[2]
        self.assertDocumentsEqual(result_doc3, self.doc4)

        result_doc4 = result_list[3]
        self.assertDocumentsEqual(result_doc4, self.doc3)

    def test_advanced_follow_only_direct_relations(self):

        document_id = self.doc1.id

        result_list = Traveser.extended_follow(
            start_vertex=document_id,
            edge_collection=self.test_1_edge_col.name,
            direction='inbound',
        )

        for result in result_list:
            print(result.ta)

        result_list = Traveser.extended_follow(
            start_vertex=document_id,
            edge_collection=self.test_1_edge_col.name,
            direction='outbound',
            max_depth=1,
        )

        # 1 -> 2 _ 4
        # 1 -> 4
        # 1 -> 3
        self.assertEqual(len(result_list), 3)

        result_doc1 = result_list[0]
        self.assertDocumentsEqual(result_doc1, self.doc2)

        result_doc2 = result_list[1]
        self.assertDocumentsEqual(result_doc2, self.doc4)

        result_doc3 = result_list[2]
        self.assertDocumentsEqual(result_doc3, self.doc3)
