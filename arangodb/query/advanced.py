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
    OR_BIT_OPERATOR = '||'
    AND_BIT_OPERATOR = '&&'

    @classmethod
    def execute_raw(cls, query_string):
        """
        """

        logger.debug(query_string)

        post_data = {
            'query': query_string
        }

        api = Client.instance().api

        result = []

        try:
            start_time = time()
            post_result = api.cursor.post(data=post_data)
            end_time = time()

            time_result = '%0.3f ms' % (end_time - start_time) * 1000
            logger.debug('Query took' + time_result)

            result_dict_list = post_result['result']

            # Create documents
            for result_list in result_dict_list:

                # Look if it is a list which needs to be iterated
                if isinstance(result_list, list):
                    for result_dict in result_list:
                        doc = create_document_from_result_dict(result_dict, api)
                        result.append(doc)
                # Otherwise just create a result document
                else:
                    result_dict = result_list
                    doc = create_document_from_result_dict(result_dict, api)
                    result.append(doc)

        except Exception as err:
            raise err

        return result

    def __init__(self):
        """
        """

        self.collections = []
        self.filters = []

        self.start = -1
        self.count = -1

        self.sorting = []

    def set_collection(self, collection_name):
        """
        """

        self.collections = [ collection_name ]

    def clear(self):
        """
        """

        # TODO: Check how to clear these lists better
        self.filters = []
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

        query_data += self._get_collection_iteration_statements()

        query_data += self._get_sorting_statement()

        if self.count is not -1:

            if self.start is not -1:
                query_data += ' LIMIT %s, %s' % (self.start, self.count)
            else:
                query_data += ' LIMIT %s' % self.count


        # Set return statement
        query_data += self._get_return_statement()

        # Execute query
        result = Query.execute_raw(query_string=query_data)

        return result


    def _get_collection_ident(self, collection_name):
        """
        """

        return collection_name + '_123'

    def _get_collection_iteration_statements(self):
        """
        """

        query_data = ''

        collection_filters = {}

        for filter_statement in self.filters:
            # We only care about the containers
            if isinstance(filter_statement, QueryFilterContainer):

                for filter in filter_statement.filters:
                    # Check if the collection is already in the filters for collections
                    if filter.collection in collection_filters:
                        container = collection_filters[filter.collection]
                        container.append(filter)
                    else:
                        container = QueryFilterContainer(bit_operator=Query.AND_BIT_OPERATOR)
                        container.filters.append(filter)

                        collection_filters[filter.collection] = container


        for collection in self.collections:
            query_data += ' FOR %s in %s' % (
                self._get_collection_ident(collection),
                collection
            )

            # If there were OR conditions this is the place where they are set
            if collection in collection_filters:
                container = collection_filters[collection]
                query_data += self._get_filter_string(container)

        for filter_statement in self.filters:

            if not isinstance(filter_statement, QueryFilterContainer):
                query_data += self._get_filter_string(filter_statement)

        return query_data

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

    def _get_return_statement(self):
        """
        """

        return_statement = ''

        if len(self.collections) is 1:
            collection = self.collections[0]
            return_statement += ' RETURN %s' % self._get_collection_ident(collection_name=collection)
        else:
            colletions_string = ''
            is_first = True

            for collection in self.collections:
                if is_first:
                    is_first = False

                    colletions_string += self._get_collection_ident(collection)

                else:
                    colletions_string += ' , %s ' % self._get_collection_ident(collection)


            return_statement += ' RETURN [ %s ]' % colletions_string

        return return_statement

    def _get_sorting_statement(self):
        """
        """

        query_data = ''
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

        return query_data


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