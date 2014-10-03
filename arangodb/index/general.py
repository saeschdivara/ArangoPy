
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


class FulltextIndex(BaseIndex):
    """
    """

    type_name = 'fulltext'

    def __init__(self, fields, minimum_length):
        """
        """

        super(FulltextIndex, self).__init__()

        self.fields = fields
        self.minimum_length = minimum_length

    def get_extra_attributes(self):
        """
        """

        return {
            'fields': self.fields,
            'minimum_length': self.minimum_length,
        }