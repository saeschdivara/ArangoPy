# -*- coding: utf-8 -*-
import logging
from time import time

from arangodb.api import Client, Document
from arangodb.query.utils.document import create_document_from_result_dict


logger = logging.getLogger(name='ArangoPy')

class QueryFilterStatement(object):
    EQUAL_OPERATOR = '=='
    NOT_EQUAL_OPERATOR = '!='

    def __init__(self, collection, attribute, operator, value):
        """
        """

        self.collection = collection
        self.attribute = attribute
        self.operator = operator
        self.value = value


class QueryFilterContainer(object):

    def __init__(self, bit_operator):
        """
        """

        self.filters = []
        self.bit_operator = bit_operator


class Query(object):
    SORTING_ASC = 'ASC'
    SORTING_DESC = 'DESC'

    NO_BIT_OPERATOR = None
    OR_BIT_OPERATOR = 'OR'
    AND_BIT_OPERATOR = 'AND'

    def __init__(self):
        """
        """

        self.collections = []
        self.filters = []

        self.start = -1
        self.count = -1

        self.sorting = []

    def append_collection(self, collection_name):
        """
        """

        self.collections.append(collection_name)

        return self

    def filter(self, bit_operator=NO_BIT_OPERATOR, **kwargs):
        """
        """

        if bit_operator == Query.NO_BIT_OPERATOR:
            filters = self.filters
        else:
            filter_container = QueryFilterContainer(bit_operator=bit_operator)
            filters = filter_container.filters
            self.filters.append(filter_container)

        for key, value in kwargs.iteritems():

            splitted_filter = key.split('__')

            if len(splitted_filter) is 1:

                filters.append(
                    QueryFilterStatement(
                        collection=self.collections[-1],
                        attribute=key,
                        operator=QueryFilterStatement.EQUAL_OPERATOR,
                        value=value,
                    )
                )

            else:

                filters.append(
                    QueryFilterStatement(
                        collection=splitted_filter[0],
                        attribute=splitted_filter[1],
                        operator=QueryFilterStatement.EQUAL_OPERATOR,
                        value=value,
                    )
                )

        return self

    def exclude(self, **kwargs):
        """
        """

        for key, value in kwargs.iteritems():

            splitted_filter = key.split('__')

            if len(splitted_filter) is 1:

                self.filters.append(
                    QueryFilterStatement(
                        collection=self.collections[-1],
                        attribute=key,
                        operator=QueryFilterStatement.NOT_EQUAL_OPERATOR,
                        value=value,
                    )
                )

            else:

                self.filters.append(
                    QueryFilterStatement(
                        collection=splitted_filter[0],
                        attribute=splitted_filter[1],
                        operator=QueryFilterStatement.NOT_EQUAL_OPERATOR,
                        value=value,
                    )
                )

        return self

    def limit(self, count, start=-1):
        """
        """

        self.start = start
        self.count = count

    def order_by(self, field, order=None, collection=None):
        """
        """

        if order is None:
            order = self.SORTING_ASC

        self.sorting.append({
            'field': field,
            'order': order,
            'collection': collection,
        })

    def execute(self):
        """
        """

        query_data = ''

        for collection in self.collections:
            query_data += ' FOR %s in %s' % (
                self._get_collection_ident(collection),
                collection
            )

        for filter_statement in self.filters:
            query_data += self._get_filter_string(filter_statement)

        is_first = True

        for sorting_entry in self.sorting:

            if is_first:
                query_data += ' SORT '

            if sorting_entry['field'] is not None:

                if not is_first:
                    query_data += ', '

                if sorting_entry['collection'] is not None:
                    query_data += '%s.%s %s' % (
                        self._get_collection_ident(sorting_entry['collection']),
                        sorting_entry['field'],
                        sorting_entry['order'],
                    )
                else:
                    query_data += '%s.%s %s' % (
                        self._get_collection_ident(self.collections[0]),
                        sorting_entry['field'],
                        sorting_entry['order'],
                    )

                if is_first:
                    is_first = False

        if self.count is not -1:

            if self.start is not -1:
                query_data += ' LIMIT %s, %s' % (self.start, self.count)
            else:
                query_data += ' LIMIT %s' % self.count

        query_data += ' RETURN %s' % collection + '_123'

        logger.debug(query_data)
        print(query_data)

        post_data = {
            'query': query_data
        }

        api = Client.instance().api

        result = []

        try:
            start_time = time()
            post_result = api.cursor.post(data=post_data)
            end_time = time()

            logger.debug("Query took %0.3f ms" % (end_time - start_time) * 1000)

            result_dict_list = post_result['result']

            # Create documents
            for result_dict in result_dict_list:
                doc = create_document_from_result_dict(result_dict, api)
                result.append(doc)


        except Exception as err:
            print(err.message)
            # raise err

        return result


    def _get_collection_ident(self, collection_name):
        """
        """

        return collection_name + '_123'

    def _get_filter_string(self, filter_statement):
        """
        """

        if isinstance(filter_statement, QueryFilterContainer):
            filter_string = ' FILTER '
            is_first = True

            for filter in filter_statement.filters:
                if is_first:
                    is_first = False

                    filter_string += self._get_filter_condition_string(filter)
                else:
                    filter_string += ' %s %s ' % (
                        filter_statement.bit_operator,
                        self._get_filter_condition_string(filter)
                    )
        else:
            filter_string = ' FILTER %s' % self._get_filter_condition_string(filter_statement)

        return filter_string

    def _get_filter_condition_string(self, filter_statement):
        """
        """

        if isinstance(filter_statement.value, basestring):
            filter_string = '%s.%s %s "%s"' % (
                self._get_collection_ident(filter_statement.collection),
                filter_statement.attribute,
                filter_statement.operator,
                filter_statement.value,
            )
        else:
            filter_string = '%s.%s %s %s' % (
                self._get_collection_ident(filter_statement.collection),
                filter_statement.attribute,
                filter_statement.operator,
                filter_statement.value,
            )

        return filter_string


class Traveser(object):
    """
    """

    @classmethod
    def follow(cls, start_vertex, edge_collection, direction):
        """
        """

        related_docs = []

        request_data = {
            'startVertex': start_vertex,
            'edgeCollection': edge_collection,
            'direction': direction,
        }

        api = Client.instance().api
        result_dict = api.traversal.post(data=request_data)
        results = result_dict['result']['visited']

        vertices = results['vertices']
        vertices.remove(vertices[0])

        for vertice in vertices:
            collection_name = vertice['_id'].split('/')[0]

            doc = Document(
                id=vertice['_id'],
                key=vertice['_key'],
                collection=collection_name,
                api=api,
            )

            del vertice['_id']
            del vertice['_key']
            del vertice['_rev']

            doc.data = vertice

            related_docs.append(doc)

        return related_docs