# -*- coding: utf-8 -*-

from arangodb.api import Client
from arangodb.query.utils.document import create_document_from_result_dict


class SimpleQuery(object):
    """
        Simple queries collection
    """


    @classmethod
    def all(cls, collection, skip=None, limit=None):
        """
            Returns all documents of the collection

            :param collection Collection instance
            :param skip  The number of documents to skip in the query
            :param limit The maximal amount of documents to return. The skip is applied before the limit restriction.

            :returns Document list
        """

        kwargs = {
            'skip': skip,
            'limit': limit,
        }

        return cls._construct_query(name='all', collection=collection, multiple=True,
                                    **kwargs)


    @classmethod
    def get_by_example(cls, collection, example_data, allow_multiple=False, skip=None, limit=None):
        """
            This will find all documents matching a given example.

            :param collection Collection instance
            :param example_data The example document
            :param allow_multiple If the query can return multiple documents
            :param skip  The number of documents to skip in the query
            :param limit The maximal amount of documents to return. The skip is applied before the limit restriction.

            :returns Single document / Document list
        """

        kwargs = {
            'skip': skip,
            'limit': limit,
        }

        return cls._construct_query(name='by-example',
                                    collection=collection, example=example_data, multiple=allow_multiple,
                                    **kwargs)


    @classmethod
    def update_by_example(cls, collection, example_data, new_value, keep_null=False, wait_for_sync=None, limit=None):
        """
            This will find all documents in the collection that match the specified example object,
            and partially update the document body with the new value specified. Note that document meta-attributes
            such as _id, _key, _from, _to etc. cannot be replaced.

            Note: the limit attribute is not supported on sharded collections. Using it will result in an error.

            Returns result dict of the request.

            :param collection Collection instance
            :param example_data An example document that all collection documents are compared against.
            :param new_value A document containing all the attributes to update in the found documents.

            :param keep_null This parameter can be used to modify the behavior when handling null values.
            Normally, null values are stored in the database. By setting the keepNull parameter to false,
            this behavior can be changed so that all attributes in data with null values will be removed
            from the updated document.

            :param wait_for_sync  if set to true, then all removal operations will instantly be synchronised to disk.
            If this is not specified, then the collection's default sync behavior will be applied.

            :param limit an optional value that determines how many documents to update at most. If limit is
            specified but is less than the number of documents in the collection, it is undefined
            which of the documents will be updated.

            :returns dict
        """

        kwargs = {
            'newValue': new_value,
            'options': {
                'keepNull': keep_null,
                'waitForSync': wait_for_sync,
                'limit': limit,
            }
        }

        return cls._construct_query(name='update-by-example',
                                    collection=collection, example=example_data, result=False,
                                    **kwargs)


    @classmethod
    def replace_by_example(cls, collection, example_data, new_value, wait_for_sync=None, limit=None):
        """
            This will find all documents in the collection that match the specified example object,
            and replace the entire document body with the new value specified. Note that document
            meta-attributes such as _id, _key, _from, _to etc. cannot be replaced.

            Note: the limit attribute is not supported on sharded collections. Using it will result in an error.
            The options attributes waitForSync and limit can given yet without an ecapsulation into a json object.
            But this may be deprecated in future versions of arango

            Returns result dict of the request.

            :param collection Collection instance
            :param example_data An example document that all collection documents are compared against.
            :param new_value The replacement document that will get inserted in place of the "old" documents.

            :param wait_for_sync  if set to true, then all removal operations will instantly be synchronised to disk.
            If this is not specified, then the collection's default sync behavior will be applied.

            :param limit an optional value that determines how many documents to replace at most. If limit is
            specified but is less than the number of documents in the collection, it is undefined which of the
            documents will be replaced.

            :returns dict
        """

        kwargs = {
            'newValue': new_value,
            'options': {
                'waitForSync': wait_for_sync,
                'limit': limit,
            }
        }

        return cls._construct_query(name='replace-by-example',
                                    collection=collection, example=example_data, result=False,
                                    **kwargs)


    @classmethod
    def remove_by_example(cls, collection, example_data, wait_for_sync=None, limit=None):
        """
        """

        kwargs = {
            'options': {
                'waitForSync': wait_for_sync,
                'limit': limit,
            }
        }

        return cls._construct_query(name='remove-by-example',
                                    collection=collection, example=example_data, result=False,
                                    **kwargs)


    @classmethod
    def random(cls, collection):
        """
        """

        return cls._construct_query(name='any', collection=collection)


    @classmethod
    def _construct_query(cls, name, collection, multiple=False, result=True, **kwargs):
        """
        """

        query = {
            'collection': collection.name,
        }

        for arg_name in kwargs:
            query[arg_name] = kwargs[arg_name]

        client = Client.instance()
        client.set_database(collection.database)
        api = client.api
        result_dict = api.simple(name).put(data=query)

        if not result:
            return result_dict

        if result_dict['count'] == 0:
            return None

        if multiple is True:

            docs = []

            for result_dict_obj in result_dict['result']:
                doc = create_document_from_result_dict(result_dict_obj, api)
                docs.append(doc)

            return docs

        else:
            return create_document_from_result_dict(result_dict['result'][0], api)


class SimpleIndexQuery(SimpleQuery):
    """
    """

    @classmethod
    def get_by_example_hash(cls, collection, index_id, example_data, allow_multiple=False, skip=None, limit=None):
        """
        """

        kwargs = {
            'index': index_id,
            'skip': skip,
            'limit': limit,
        }

        return cls._construct_query(name='by-example-hash',
                                    collection=collection, example=example_data, multiple=allow_multiple,
                                    **kwargs)

    @classmethod
    def get_by_example_skiplist(cls, collection, index_id, example_data, allow_multiple=True, skip=None, limit=None):
        """
        """

        kwargs = {
            'index': index_id,
            'skip': skip,
            'limit': limit,
        }

        return cls._construct_query(name='by-example-skiplist',
                                    collection=collection, example=example_data, multiple=allow_multiple,
                                    **kwargs)

    @classmethod
    def range(cls, collection, attribute, left, right, closed, index_id, skip=None, limit=None):
        """
        """

        kwargs = {
            'index': index_id,
            'attribute': attribute,
            'left': left,
            'right': right,
            'closed': closed,
            'skip': skip,
            'limit': limit,
        }

        return cls._construct_query(name='range',
                                    collection=collection, multiple=True,
                                    **kwargs)

    @classmethod
    def fulltext(cls, collection, attribute, example_text, index_id, skip=None, limit=None):
        """
        """

        kwargs = {
            'index': index_id,
            'attribute': attribute,
            'query': example_text,
            'skip': skip,
            'limit': limit,
        }

        return cls._construct_query(name='fulltext',
                                    collection=collection, multiple=True,
                                    **kwargs)

    @classmethod
    def near(cls, collection, latitude, longitude, index_id, distance=None, skip=None, limit=None):
        """
        """

        kwargs = {
            'geo': index_id,
            'latitude': latitude,
            'longitude': longitude,
            'distance': distance,
            'skip': skip,
            'limit': limit,
        }

        return cls._construct_query(name='near',
                                    collection=collection, multiple=True,
                                    **kwargs)

    @classmethod
    def within(cls, collection, latitude, longitude, radius, index_id, distance=None, skip=None, limit=None):
        """
        """

        kwargs = {
            'geo': index_id,
            'latitude': latitude,
            'longitude': longitude,
            'radius': radius,
            'distance': distance,
            'skip': skip,
            'limit': limit,
        }

        return cls._construct_query(name='within',
                                    collection=collection, multiple=True,
                                    **kwargs)

