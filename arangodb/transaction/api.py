from arangodb.transaction.action import DocumentAction


class TransactionDatabase(object):
    """
    """

    def __init__(self, name, transaction):
        """
        """

        self.name = name
        self.transaction = transaction

    def collection(self, name):
        """
        """

        return TransactionCollection(name=name, transaction=self.transaction)


class TransactionCollection(object):
    """
    """

    def __init__(self, name, transaction):
        """
        """

        self.name = name
        self.transaction = transaction

    def create_document(self, data):
        """
        """

        action = DocumentAction.create(collection_name=self.name, document_data=data)
        self.transaction.add_action(action=action)

        doc = TransactionDocument(data=data, action=action)
        return doc



class TransactionDocument(object):
    """
    """

    def __init__(self, data, action):
        """
        """

        self.data = data
        self._action = action