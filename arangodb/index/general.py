
class BaseIndex(object):
    """
        This is the base class for all other index
        but which has no functionality
    """

    type_name = None

    def __init__(self):
        """
        """

        self.id = None
        self.is_new = False

    def get_extra_attributes(self):
        """
            You need to override this method for each index
            so it can return a dict with all values which are needed
            for the index
        """


class FulltextIndex(BaseIndex):
    """
        Index for fulltext search
    """

    type_name = 'fulltext'

    def __init__(self, fields, minimum_length):
        """
            Creates fulltext index which is configured for the fields with
            the minimum word length

            :param fields A list of attribute names. Currently, the list is limited to exactly one attribute, so the
            value of fields should look like this for example: [ "text" ].

            :param minimum_length Minimum character length of words to index. Will default to a server-defined value
            if unspecified. It is thus recommended to set this value explicitly when creating the index.

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
    """
        The cap constraint does not index particular attributes of the documents in a collection,
        but limits the number of documents in the collection to a maximum value.
        The cap constraint thus does not support attribute names specified in the fields attribute
        nor uniqueness of any kind via the unique attribute.
    """

    type_name = 'cap'

    def __init__(self, size, document_byte_size=16384):
        """
            :param size  The maximal number of documents for the collection. If specified, the value
            must be greater than zero.

            :param document_byte_size The maximal size of the active document data in the collection (in bytes).
            If specified, the value must be at least 16384.
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
