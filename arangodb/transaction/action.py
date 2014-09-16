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

    def __init__(self, action_type):
        super(CollectionAction, self).__init__(action_type)

    @classmethod
    def create(cls):
        return cls(action_type='create')