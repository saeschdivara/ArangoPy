from arangodb.index.general import BaseIndex


class HashIndex(BaseIndex):
    """
    """

    type_name = 'hash'

    def __init__(self, fields, unique=True):
        """
        """

        super(HashIndex, self).__init__()

        self.fields = fields
        self.unique = unique

    def get_extra_attributes(self):
        """
        """

        return {
            'fields': self.fields,
            'unique': self.unique,
        }


class SkiplistIndex(HashIndex):
    """
    """

    type_name = 'skiplist'