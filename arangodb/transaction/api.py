class TransactionDatabase(object):
    """
    """

    def __init__(self, name, transaction):
        """
        """

        self.name = name
        self.transaction = transaction

    def create_collection(self, name):
        """
        """

        self.transaction.add_action(action='')
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