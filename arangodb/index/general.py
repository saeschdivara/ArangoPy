
class BaseIndex(object):
    """
    """

    type_name = None

    def __init__(self):
        """
        """

        self.id = None
        self.is_new = False

    def get_extra_attributes(self):
        """
        """

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