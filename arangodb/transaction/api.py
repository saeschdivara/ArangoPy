from arangodb.transaction.action import CollectionAction


class TransactionDatabase(object):
    """
    """

    def __init__(self, name, transaction):
        """
        """

        self.name = name
        self.transaction = transaction

    def create_collection(self, name, type=2):
        """
        """

        self.transaction.add_action(action=CollectionAction.create(name=name, database=self.name, collection_type=type))
        return TransactionCollection(name=name, transaction=self.transaction)


class TransactionCollection(object):
    """
    """

    def __init__(self, name, transaction):
        """
        """

        self.name = name
        self.transaction = transaction


class TransactionDocument(object):
    """
    """