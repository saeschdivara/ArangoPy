class TransactionAction(object):
    """
    """

    def __init__(self, action_type):
        self.action_type = action_type


class DocumentAction(TransactionAction):
    """
    """

    def __init__(self, action_type, collection_name, document_data):
        """
        """

        super(DocumentAction, self).__init__(action_type)

        self.collection_name = collection_name
        self.document_data = document_data

    @classmethod
    def create(cls, collection_name, document_data):
        """
        """

        return cls(action_type='create', collection_name=collection_name, document_data=document_data)