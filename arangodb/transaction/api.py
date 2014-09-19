from arangodb.transaction.action import DocumentAction


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

    def update_document(self, doc_id, data):
        """
        """

        action = DocumentAction.update(collection_name=self.name, _id=doc_id, document_data=data)
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