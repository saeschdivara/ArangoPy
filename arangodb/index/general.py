
class BaseIndex(object):
    """
    """

    type_name = None

    def get_extra_attributes(self):
        """
        """

        return {}

class HashIndex(BaseIndex):
    """
    """

    type_name = 'hash'

    def __init__(self, fields, unique=True):
        """
        """

        self.fields = fields
        self.unique = unique

    def get_extra_attributes(self):
        """
        """

        return {
            'fields': self.fields,
            'unique': self.unique,
        }