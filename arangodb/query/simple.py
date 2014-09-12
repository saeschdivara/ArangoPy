# -*- coding: utf-8 -*-

from api import Client
from query.utils.document import create_document_from_result_dict


class SimpleQuery(object):
    """
    """


    @classmethod
    def all(cls, collection):
        """
        """


    @classmethod
    def getByExample(cls, collection, example_data):
        """
        """

        return SimpleQuery._construct_query(name='by-example', collection=collection, example=example_data)


    @classmethod
    def random(cls, collection):
        """
        """

        return SimpleQuery._construct_query(name='any', collection=collection)


    @classmethod
    def _construct_query(cls, name, collection, **kwargs):
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

        try:
            return create_document_from_result_dict(result_dict['result'][0], api)
        except:
            return result_dict