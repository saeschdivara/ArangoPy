from arangodb.api import Collection


class ModelField(object):

    def __init__(self, is_required=True):
        """
        """

        self.is_required = is_required

class CollectionModel(object):

    collection_instance = None
    collection_name = None

    @classmethod
    def init(cls):

        if cls.collection_name is not None and len(cls.collection_name) > 0:
            name = cls.collection_name
        else:
            name = cls.__name__

        try:
            collection_type = getattr(cls, 'collection_type')
        except:
            collection_type = 2

        try:
            cls.collection_instance = Collection.create(name=name, type=collection_type)
        except:
            cls.collection_instance = Collection.get_loaded_collection(name=name)

        return cls()

    def __init__(self):
        """
        """

        self.document = self.collection_instance.create_document()

    def save(self):
        """
        """

        for attribute in self.__dict__:
            print(attribute)