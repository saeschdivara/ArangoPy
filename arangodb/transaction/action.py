class TransactionAction(object):
    """
    """

    base_type = None

    def __init__(self, action_type):
        self.action_type = action_type


class CollectionAction(TransactionAction):
    """
    """

    base_type = 'collection'

    def __init__(self, action_type, name, database, collection_type):
        """
        """

        super(CollectionAction, self).__init__(action_type)

        self.name = name
        self.database = database
        self.collection_type = collection_type

    @classmethod
    def create(cls, name, database, collection_type=2):
        """
        """

        return cls(action_type='create', name=name, database=database, collection_type=collection_type)