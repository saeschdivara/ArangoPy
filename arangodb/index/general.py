
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
            'minLength': self.minimum_length,
        }


class CapConstraintIndex(BaseIndex):

    type_name = 'cap'

    def __init__(self, size, document_byte_size=16384):
        """
        """

        super(CapConstraintIndex, self).__init__()

        self.size = size
        self.document_byte_size = document_byte_size

    def get_extra_attributes(self):
        """
        """

        return {
            'size': self.size,
            'byteSize': self.document_byte_size,
        }
