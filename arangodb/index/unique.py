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


class GeoIndex(HashIndex):
    """
    """

    type_name = 'geo'

    def __init__(self, fields, geo_json, ignore_null=True, unique=True):
        """
        """

        super(GeoIndex, self).__init__(fields, unique)

        self.geo_json = geo_json
        self.ignore_null = ignore_null

    def get_extra_attributes(self):
        """
        """

        return {
            'fields': self.fields,
            'unique': self.unique,
            'geoJson': self.geo_json,
            'ignoreNull': self.ignore_null,
        }