from arangodb.api import Client


class Index(object):
    """
    """

    @classmethod
    def remove(cls, id):
        """
            Deletes an index with id

            :param id string/document-handle
        """

        api = Client.instance().api
        api.index(id).delete()

    def __init__(self, collection, index_type_obj):
        """
            Constructs wrapper for general index creation and deletion

            :param collection Collection
            :param index_type_obj BaseIndex Object of a index sub-class
        """

        self.collection = collection
        self.index_type_obj = index_type_obj

    def save(self):
        """
            Creates this index in the collection if it hasn't been already created
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
            Deletes this index
        """

        Index.remove(self.index_type_obj.id)

    def overwrite(self):
        """
            Deletes and creates again this index so it will have the current configuration
        """

        self.delete()
        self.save()