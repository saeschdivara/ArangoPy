class TransactionAction(object):
    """
    """

    base_type = None

    def __init__(self):
        pass


class CollectionAction(TransactionAction):
    """
    """

    base_type = 'collection'

    def __init__(self):
        super(CollectionAction, self).__init__()