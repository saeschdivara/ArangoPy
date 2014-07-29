from arangodb.api import Collection


class ModelField(object):

    def __init__(self, is_required=True, **kwargs):
        """
        """

        self.is_required = is_required

    def dumps(self):
        """
        """

        return u''

    def loads(self, string_val):
        """
        """

        pass

    def set(self, *args, **kwargs):
        """
        """

        pass

class TextField(ModelField):

    def __init__(self, is_required=True, **kwargs):
        """
        """

        super(TextField, self).__init__(**kwargs)

        self.text = u''

    def dumps(self):
        """
        """

        return u'%s' % self.text

    def loads(self, string_val):
        """
        """

        self.text = string_val

    def set(self, *args, **kwargs):
        """
        """

        if len(args) is 1:
            self.text = args[0]

class CollectionModel(object):

    collection_instance = None
    collection_name = None

    @classmethod
    def init(cls):

        name = cls.get_collection_name()

        try:
            collection_type = getattr(cls, 'collection_type')
        except:
            collection_type = 2

        try:
            cls.collection_instance = Collection.create(name=name, type=collection_type)
        except:
            cls.collection_instance = Collection.get_loaded_collection(name=name)

    @classmethod
    def destroy(cls):
        name = cls.get_collection_name()
        Collection.remove(name=name)

    @classmethod
    def get_collection_name(cls):

        if cls.collection_name is not None and len(cls.collection_name) > 0:
            name = cls.collection_name
        else:
            name = cls.__name__

        return name

    def __init__(self):
        """
        """

        self.document = self.collection_instance.create_document()

    def save(self):
        """
        """

        all_fields = self._get_fields()

        for field_name in all_fields:
            field = all_fields[field_name]
            field_value = field.dumps()

            self.document.set(key=field_name, value=field_value)

        self.document.save()

    def _get_fields(self):
        fields = {}

        for attribute in dir(self):

            attr_val = getattr(self, attribute)
            attr_cls = attr_val.__class__

            if issubclass(attr_cls, ModelField):
                fields[attribute] = attr_val

        return fields