from arangodb.api import Client


class Index(object):
    """
    """

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
        print(result)