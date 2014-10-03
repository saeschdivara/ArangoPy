from arangodb.api import Client


class Index(object):
    """
    """

    @classmethod
    def remove(cls, id):
        """
        """

        api = Client.instance().api
        api.index(id).delete()

    def __init__(self, collection, index_type_obj):
        """
        """

        self.collection = collection
        self.index_type_obj = index_type_obj

    def save(self):
        """
        """

        api = Client.instance().api

        index_details = {
            'type': self.index_type_obj.type_name
        }

        extra_index_attributes = self.index_type_obj.get_extra_attributes()

        for extra_attribute_key in extra_index_attributes:
            extra_attribute_value = extra_index_attributes[extra_attribute_key]
            index_details[extra_attribute_key] = extra_attribute_value

        query_parameters = {
            'collection': self.collection.name,
        }

        result = api.index.post(data=index_details, **query_parameters)

        self.index_type_obj.is_new = result['isNewlyCreated']
        self.index_type_obj.id = result['id']

    def delete(self):
        """
        """

        Index.remove(self.index_type_obj.id)