# -*- coding: utf-8 -*-
import logging
from time import time
from arangodb import six

from arangodb.api import Client, Document
from arangodb.query.utils.document import create_document_from_result_dict


logger = logging.getLogger(name='ArangoPy')

class QueryFilterStatement(object):
    EQUAL_OPERATOR = '=='
    NOT_EQUAL_OPERATOR = '!='

    QUERY_CONDITION_EXTENSIONS = {
        'exact': EQUAL_OPERATOR,
        'gt': '>',
        'gte': '>=',
        'lt': '<',
        'lte': '<=',
    }

    QUERY_FUNCTION_EXTENSIONS = ( 'contains', 'icontains', )

    def __init__(self, collection, attribute, value, **kwargs):
        """
        """

        self.collection = collection
        self.attribute = attribute

        if 'operator' in kwargs:
            self.operator = kwargs['operator']
        else:
            self.operator = None

        if 'function' in kwargs:
            self.function = kwargs['function']
        else:
            self.function = None

        self.value = value


    def get_filter_function_string(self, collection_name):
        """
        """

        if self.function == 'contains':

            filter_string = ' CONTAINS (%s.%s, %s) ' % (
                        collection_name,
                        self.attribute,
                        self.get_value_string(),
                    )

        elif self.function == 'icontains':

            filter_string = ' LIKE (%s.%s, "%s%s%s", true) ' % (
                        collection_name,
                        self.attribute,
                        '%',
                        self.value,
                        '%',
                    )

        else:
            filter_string = ''

        return filter_string


    def get_value_string(self):
        """
        """

        if isinstance(self.value, six.string_types):
            return '"%s"' % self.value
        else:
            return '%s' % self.value


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

            calculated_time = (end_time - start_time) * 1000
            time_result = '%s ms' % calculated_time
            logger_output = 'Query took %s' % time_result
            logger.debug(logger_output)

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

        for key, value in six.iteritems(kwargs):

                filters.append(
                    self._get_filter_statement(key, value, QueryFilterStatement.EQUAL_OPERATOR)
                )

        return self

    def exclude(self, **kwargs):
        """
        """

        for key, value in six.iteritems(kwargs):

            self.filters.append(
                self._get_filter_statement(key, value, QueryFilterStatement.NOT_EQUAL_OPERATOR)
            )

        return self

    def _get_filter_statement(self, filter_string, filter_value, default_operator):
        """
        """

        splitted_filter = filter_string.split('__')

        lenght_splitted_filter = len(splitted_filter)

        if lenght_splitted_filter is 1:

            return QueryFilterStatement(
                collection=self.collections[-1],
                attribute=filter_string,
                operator=default_operator,
                value=filter_value,
            )

        else:

            if lenght_splitted_filter is 2:

                second_filter_value = splitted_filter[1]

                # Is this a normal condition
                if second_filter_value in QueryFilterStatement.QUERY_CONDITION_EXTENSIONS:

                    operator = QueryFilterStatement.QUERY_CONDITION_EXTENSIONS[ second_filter_value ]

                    return QueryFilterStatement(
                        collection=self.collections[-1],
                        attribute=splitted_filter[0],
                        operator=operator,
                        value=filter_value,
                    )

                # Is this a function condition
                elif second_filter_value in QueryFilterStatement.QUERY_FUNCTION_EXTENSIONS:

                    return QueryFilterStatement(
                        collection=self.collections[-1],
                        attribute=splitted_filter[0],
                        function=second_filter_value,
                        value=filter_value,
                    )

                # Just collection and attribute
                else:
                    return QueryFilterStatement(
                        collection=splitted_filter[0],
                        attribute=second_filter_value,
                        operator=default_operator,
                        value=filter_value,
                    )


            else:


                if splitted_filter[2] in QueryFilterStatement.QUERY_CONDITION_EXTENSIONS:
                    operator = QueryFilterStatement.QUERY_CONDITION_EXTENSIONS[ splitted_filter[2] ]

                    return QueryFilterStatement(
                        collection=splitted_filter[0],
                        attribute=splitted_filter[1],
                        operator=operator,
                        value=filter_value,
                    )

                # Is this a function condition
                elif splitted_filter[2] in QueryFilterStatement.QUERY_FUNCTION_EXTENSIONS:

                    return QueryFilterStatement(
                        collection=self.collections[-1],
                        attribute=splitted_filter[0],
                        function=splitted_filter[2],
                        value=filter_value,
                    )

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
                        container.filters.append(filter)
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

        filter_string = ''

        # Operator
        if not filter_statement.operator is None:
            if isinstance(filter_statement.value, six.string_types):
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
        elif not filter_statement.function is None:
            collection_name = self._get_collection_ident(filter_statement.collection)
            filter_string =  filter_statement.get_filter_function_string(collection_name)

        return filter_string

    def _get_return_statement(self):
        """
        """

        return_statement = ''

        if len(self.collections) is 1:
            collection = self.collections[0]
            return_statement += ' RETURN %s' % self._get_collection_ident(collection_name=collection)
        else:
            collections_string = ''
            is_first = True

            for collection in self.collections:
                if is_first:
                    is_first = False

                    collections_string += self._get_collection_ident(collection)

                else:
                    collections_string += ' , %s ' % self._get_collection_ident(collection)


            return_statement += ' RETURN [ %s ]' % collections_string

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

        request_data = {
            'startVertex': start_vertex,
            'edgeCollection': edge_collection,
            'direction': direction,
        }

        return Traveser._send_follow(request_data=request_data)

    @classmethod
    def extended_follow(cls, start_vertex, edge_collection, graph_name=None, **kwargs):
        """

            :param start_vertex id of the startVertex, e.g. "users/foo".
            :param edge_collection *Deprecated* name of the collection that contains the edges.
            :param graph_name name of the graph that contains the edges.

            Optionals:
            :param filter  (optional, default is to include all nodes): body (JavaScript code) of custom filter
            function function signature: (config, vertex, path) -> mixed can return four different string values:
            - "exclude" -> this vertex will not be visited.
            - "prune" -> the edges of this vertex will not be followed.
            - "" or undefined -> visit the vertex and follow it's edges.
            - Array -> containing any combination of the above. If there is at least one "exclude" or "prune"
            respectively is contained, it's effect will occur.

            :param min_depth (optional, ANDed with any existing filters): visits only nodes in at least the given depth
            :param max_depth  (optional, ANDed with any existing filters): visits only nodes in at most the given depth

            :param visitor  (optional): body (JavaScript) code of custom visitor function function signature:
            (config, result, vertex, path) -> void visitor function can do anything, but its return value is ignored.
            To populate a result, use the result variable by reference

            :param direction  (optional): direction for traversal - if set, must be either
            "outbound", "inbound", or "any" - if not set, the expander attribute must be specified

            :param init (optional): body (JavaScript) code of custom result initialisation function function signature:
            (config, result) -> void initialise any values in result with what is required

            :param expander (optional): body (JavaScript) code of custom expander function must be set if direction
            attribute is *not* set function signature: (config, vertex, path) -> array expander must return an array
            of the connections for vertex each connection is an object with the attributes edge and vertex

            :param sort (optional): body (JavaScript) code of a custom comparison function for the edges.
            The signature of this function is (l, r) -> integer (where l and r are edges) and must return -1 if l
            is smaller than, +1 if l is greater than, and 0 if l and r are equal. The reason for this is the following:
            The order of edges returned for a certain vertex is undefined. This is because there is no natural order
            of edges for a vertex with multiple connected edges. To explicitly define the order in which edges on
            the vertex are followed, you can specify an edge comparator function with this attribute. Note that the
            value here has to be a string to conform to the JSON standard, which in turn is parsed as function body
            on the server side. Furthermore note that this attribute is only used for the standard expanders. If
            you use your custom expander you have to do the sorting yourself within the expander code.

            :param strategy (optional): traversal strategy can be "depthfirst" or "breadthfirst"
            :param order (optional): traversal order can be "preorder" or "postorder"
            :param item_order (optional): item iteration order can be "forward" or "backward"

            :param uniqueness (optional): specifies uniqueness for vertices and edges visited if set, must be an object
            like this: "uniqueness": {"vertices": "none"|"global"|path", "edges": "none"|"global"|"path"}

            :param max_iterations (optional): Maximum number of iterations in each traversal.
            This number can be set to prevent endless loops in traversal of cyclic graphs. When a traversal
            performs as many iterations as the max_iterations value, the traversal will abort with an error.
            If max_iterations is not set, a server-defined value may be used.
        """

        request_data = {
            'startVertex': start_vertex,
            'edgeCollection': edge_collection,
        }

        if graph_name:
            request_data['graphName'] = graph_name

        # Set search data
        option_name = 'filter'
        if option_name in kwargs:
            request_data['filter'] = kwargs[option_name]

        option_name = 'min_depth'
        if option_name in kwargs:
            request_data['minDepth'] = kwargs[option_name]

        option_name = 'max_depth'
        if option_name in kwargs:
            request_data['maxDepth'] = kwargs[option_name]

        option_name = 'visitor'
        if option_name in kwargs:
            request_data['visitor'] = kwargs[option_name]

        option_name = 'direction'
        if option_name in kwargs:
            request_data['direction'] = kwargs[option_name]

        option_name = 'init'
        if option_name in kwargs:
            request_data['init'] = kwargs[option_name]

        option_name = 'expander'
        if option_name in kwargs:
            request_data['expander'] = kwargs[option_name]

        option_name = 'sort'
        if option_name in kwargs:
            request_data['sort'] = kwargs[option_name]

        option_name = 'strategy'
        if option_name in kwargs:
            request_data['strategy'] = kwargs[option_name]

        option_name = 'order'
        if option_name in kwargs:
            request_data['order'] = kwargs[option_name]

        option_name = 'item_order'
        if option_name in kwargs:
            request_data['itemOrder'] = kwargs[option_name]

        option_name = 'uniqueness'
        if option_name in kwargs:
            request_data['uniqueness'] = kwargs[option_name]

        option_name = 'max_iterations'
        if option_name in kwargs:
            request_data['maxIterations'] = kwargs[option_name]

        # Make tests
        if not 'direction' in kwargs and not 'expander' in kwargs:
            raise Exception('Either direction or expander have to be set')

        if 'direction' in kwargs and 'expander' in kwargs:
            raise Exception('Either direction or expander have to be set')

        return Traveser._send_follow(request_data=request_data)

    @classmethod
    def _send_follow(cls, request_data):
        """
        """

        related_docs = []

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