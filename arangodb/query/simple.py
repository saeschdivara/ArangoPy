# -*- coding: utf-8 -*-

from arangodb.api import Client
from arangodb.query.utils.document import create_document_from_result_dict


class SimpleQuery(object):
    """
    """


    @classmethod
    def all(cls, collection):
        """
        """

        return cls._construct_query(name='all', collection=collection, multiple=True)


    @classmethod
    def get_by_example(cls, collection, example_data, allow_multiple=False, skip=None, limit=None):
        """
        """

        kwargs = {
            'skip': skip,
            'limit': limit,
        }

        return cls._construct_query(name='by-example',
                                    collection=collection, example=example_data, multiple=allow_multiple,
                                    **kwargs)


    @classmethod
    def random(cls, collection):
        """
        """

        return cls._construct_query(name='any', collection=collection)


    @classmethod
    def _construct_query(cls, name, collection, multiple=False, **kwargs):
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

        if result_dict['count'] == 0:
            return None

        if multiple is True:

            docs = []

            for result_dict_obj in result_dict['result']:
                doc = create_document_from_result_dict(result_dict_obj, api)
                docs.append(doc)

            return docs

        else:
            try:
                return create_document_from_result_dict(result_dict['result'][0], api)
            except:
                return result_dict