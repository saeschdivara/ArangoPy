from arangodb.api import Collection


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
            collection_type = cls.collection_type
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

        pass
