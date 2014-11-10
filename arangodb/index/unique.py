from arangodb.index.general import BaseIndex


class HashIndex(BaseIndex):
    """
    """

    type_name = 'hash'

    def __init__(self, fields, unique=True):
        """
            *Note*: unique indexes on non-shard keys are not supported in a cluster.

            :param fields A list of attribute paths.
            :param unique  If true, then create a unique index.
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
        Skiplists are almost the same except that it can contain ranges.
    """

    type_name = 'skiplist'


class BitarrayIndex(HashIndex):
    """
        Bitarray
    """

    type_name = 'bitarray'

    def __init__(self, fields):
        """
            *Note*: unique indexes on non-shard keys are not supported in a cluster.

            :param fields A list of pairs. A pair consists of an attribute path followed by a list of values.
        """

        super(BitarrayIndex, self).__init__()

        self.fields = fields
        self.unique = False


class GeoIndex(HashIndex):
    """
    """

    type_name = 'geo'

    def __init__(self, fields, geo_json, ignore_null=True, unique=True):
        """
            *Note*: Unique indexes on non-shard keys are not supported in a cluster.

            :param fields A list with one or two attribute paths. If it is a list with one attribute path location,
            then a geo-spatial index on all documents is created using location as path to the coordinates.
            The value of the attribute must be a list with at least two double values.
            The list must contain the latitude (first value) and the longitude (second value).
            All documents, which do not have the attribute path or with value that are not suitable, are ignored.
            If it is a list with two attribute paths latitude and longitude, then a geo-spatial index on all
            documents is created using latitude and longitude as paths the latitude and the longitude.
            The value of the attribute latitude and of the attribute longitude must a double. All documents,
            which do not have the attribute paths or which values are not suitable, are ignored.

            :param geo_json If a geo-spatial index on a location is constructed and geoJson is true, then the order
            within the list is longitude followed by latitude. This corresponds to the
            format described in http://geojson.org/geojson-spec.html#positions

            :param ignore_null If a geo-spatial constraint is created and ignoreNull is true,
            then documents with a null in location or at least one null in latitude or longitude are ignored.
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