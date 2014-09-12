# -*- coding: utf-8 -*-

from api import Client
from query.utils.document import create_document_from_result_dict


class SimpleQuery(object):
    @classmethod
    def getByExample(cls, collection, example_data):
        """
        """

        query = {
            'collection': collection.name,
            'example': example_data,
        }

        client = Client.instance()
        client.set_database(collection.database)
        api = client.api
        result_dict = api.simple('by-example').put(data=query)

        if result_dict['count'] == 0:
            return None

        try:
            return create_document_from_result_dict(result_dict['result'][0], api)
        except:
            return result_dict


    @classmethod
    def random(cls, collection):
        """
        """

        query = {
            'collection': collection,
        }

        api = Client.instance().api
        result_dict = api.simple('any').put(data=query)

        if result_dict['count'] == 0:
            return None

        try:
            return create_document_from_result_dict(result_dict['result'][0], api)
        except:
            return result_dict