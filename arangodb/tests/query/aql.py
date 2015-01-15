from arangodb.api import Database, Collection
from arangodb.query.advanced import Query
from arangodb.tests.base import ExtendedTestCase


class AqlQueryTestCase(ExtendedTestCase):
    def setUp(self):
        self.database_name = 'testcase_aqlquery_123'
        self.db = Database.create(name=self.database_name)

        self.test_1_col = self.db.create_collection('foo_1')
        self.test_2_col = self.db.create_collection('foo_2')

        self.col1_doc1 = self.test_1_col.create_document()
        self.col1_doc1.little_number = 33
        self.col1_doc1.loved = False
        self.col1_doc1.small_text = "lll aa"
        self.col1_doc1.save()

        self.col1_doc2 = self.test_1_col.create_document()
        self.col1_doc2.little_number = 1
        self.col1_doc2.loved = False
        self.col1_doc2.small_text = "aaa aa"
        self.col1_doc2.save()

        self.col1_doc3 = self.test_1_col.create_document()
        self.col1_doc3.little_number = 3
        self.col1_doc3.loved = True
        self.col1_doc3.small_text = "xxx tt"
        self.col1_doc3.save()

        self.col2_doc1 = self.test_2_col.create_document()
        self.col2_doc1.little_number = 33
        self.col2_doc1.loved = False
        self.col2_doc1.save()

        self.col2_doc2 = self.test_2_col.create_document()
        self.col2_doc2.little_number = 11
        self.col2_doc2.loved = True
        self.col2_doc2.save()

    def tearDown(self):
        # They need to be deleted
        Collection.remove(name=self.test_1_col.name)
        Collection.remove(name=self.test_2_col.name)

        Database.remove(name=self.database_name)

    def test_get_all_doc_from_1_collection(self):
        q = Query()
        q.append_collection(self.test_2_col.name)
        docs = q.execute()

        self.assertEqual(len(docs), 2)

    def test_filter_number_field_in_document(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(little_number=self.col1_doc3.little_number)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc = docs[0]
        self.assertDocumentsEqual(doc, self.col1_doc3)

    def test_filter_string_field_in_document(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(small_text=self.col1_doc2.small_text)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc = docs[0]
        self.assertDocumentsEqual(doc, self.col1_doc2)

    def test_filter_of_multiple_collections(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.append_collection(self.test_2_col.name)

        dynamic_filter_dict = {}
        col_1_filter_name = "%s__%s" % (self.test_1_col.name, "little_number")
        col_2_filter_name = "%s__%s" % (self.test_2_col.name, "little_number")

        dynamic_filter_dict[col_1_filter_name] = 33
        dynamic_filter_dict[col_2_filter_name] = 33
        q.filter(bit_operator=Query.OR_BIT_OPERATOR, **dynamic_filter_dict)

        docs = q.execute()

        self.assertEqual(len(docs), 2)

        doc1 = docs[0]
        doc2 = docs[1]

        self.assertNotEqual(doc1.id, doc2.id)

        self.assertEqual(doc1.little_number, 33)
        self.assertEqual(doc2.little_number, 33)

    def test_exclude_document_from_list(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.exclude(loved=False)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc1 = docs[0]

        self.assertDocumentsEqual(doc1, self.col1_doc3)

    def test_sorting_asc_document_list(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.order_by('little_number')

        docs = q.execute()

        self.assertEqual(len(docs), 3)

        doc1 = docs[0]
        doc2 = docs[1]
        doc3 = docs[2]

        self.assertDocumentsEqual(doc1, self.col1_doc2)
        self.assertDocumentsEqual(doc2, self.col1_doc3)
        self.assertDocumentsEqual(doc3, self.col1_doc1)

    def test_limit_simple_list(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.order_by('little_number')
        q.limit(count=1)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc1 = docs[0]

        self.assertDocumentsEqual(doc1, self.col1_doc2)

    def test_limit_with_start_simple_list(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.order_by('little_number')
        q.limit(count=1, start=1)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc1 = docs[0]

        self.assertDocumentsEqual(doc1, self.col1_doc3)

    def test_greater_filtering(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(little_number__gt=20)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        self.assertDocumentsEqual(self.col1_doc1, docs[0])

    def test_greater_equals_filtering(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(little_number__gte=3)

        docs = q.execute()

        self.assertEqual(len(docs), 2)

    def test_lower_filtering(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(little_number__lt=3)

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        self.assertDocumentsEqual(self.col1_doc2, docs[0])

    def test_lower_equals_filtering(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(little_number__lte=3)

        docs = q.execute()

        self.assertEqual(len(docs), 2)

    def test_contains_filtering(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(small_text__contains='ll')

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc1 = docs[0]
        self.assertDocumentsEqual(doc1, self.col1_doc1)

    def test_icontains_filtering(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.filter(small_text__icontains='LL')

        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc1 = docs[0]
        self.assertDocumentsEqual(doc1, self.col1_doc1)