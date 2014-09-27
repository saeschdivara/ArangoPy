import copy

from arangodb.api import Collection
from arangodb.orm.fields import ModelField
from arangodb.query.advanced import Query
from arangodb.query.simple import SimpleQuery


class CollectionQueryset(object):
    """
    """

    def __init__(self, manager):
        """
        """

        self._manager = manager
        self._collection = manager._model_class.collection_instance
        self._query = Query()
        # Cache
        self._has_cache = False
        self._cache = []

    def all(self):
        """
        """

        self._has_cache = False

        self._query.set_collection(self._collection.name)
        self._query.clear()

    def _generate_cache(self):
        """
        """

        self._cache = [] # TODO: Check how to best clear this list
        self._has_cache = True

        result = self._query.execute()

        for doc in result:
            model = self._manager._create_model_from_doc(doc=doc)
            self._cache.append(model)

    def __getitem__(self, item):
        """
            Is used for the index access
        """

        if not self._has_cache:
            self._generate_cache()

        return self._cache[item]

    def __len__(self):
        """
        """

        if not self._has_cache:
            self._generate_cache()

        return len(self._cache)

class CollectionModelManager(object):

    def __init__(self, cls):
        """
        """

        self._model_class = cls

    def get(self, **kwargs):
        """
        """

        collection = self._model_class.collection_instance

        doc = SimpleQuery.get_by_example(collection=collection, example_data=kwargs)

        if doc is None:
            return None

        model = self._create_model_from_doc(doc=doc)

        return model

    def all(self):
        """
        """

        queryset = CollectionQueryset(manager=self)
        queryset.all()

        return queryset

        # docs = self._model_class.collection_instance.documents()
        # models = []
        #
        # for doc in docs:
        #     model = self._create_model_from_doc(doc=doc)
        #     models.append(model)
        #
        # return models


    def _create_model_from_doc(self, doc):
        """
        """

        doc.retrieve()

        attributes = doc.get_attributes()

        model = self._create_model_from_dict(attribute_dict=attributes)

        return model


    def _create_model_from_dict(self, attribute_dict):
        """
        """

        model = self._model_class()

        attributes = attribute_dict
        for attribute_name in attributes:

            if not attribute_name.startswith('_'):
                field = model.get_field(name=attribute_name)
                attribute_value = attributes[attribute_name]
                field._model_instance = self._model_class
                field.loads(attribute_value)

        return model


class CollectionModel(object):

    collection_instance = None
    collection_name = None

    objects = CollectionModelManager

    _instance_meta_data = None

    class RequiredFieldNoValue(Exception):
        """
            Field needs value
        """


    class MetaDataObj(object):

        def __init__(self):
            self._fields = {}

    @classmethod
    def init(cls):
        """
        """

        name = cls.get_collection_name()

        try:
            collection_type = getattr(cls, 'collection_type')
        except:
            collection_type = 2

        try:
            cls.collection_instance = Collection.create(name=name, type=collection_type)
        except:
            cls.collection_instance = Collection.get_loaded_collection(name=name)

        try:
            if not isinstance(cls.objects, CollectionModelManager):
                cls.objects = cls.objects(cls)
        except:
            pass # This is the case if init was called more than once

    @classmethod
    def destroy(cls):
        """
        """

        name = cls.get_collection_name()
        Collection.remove(name=name)

    @classmethod
    def get_collection_name(cls):
        """
        """

        if cls.collection_name is not None and len(cls.collection_name) > 0:
            name = cls.collection_name
        else:
            name = cls.__name__

        return name

    def __init__(self):
        """
        """

        # _instance_meta_data has to be set first otherwise the whole thing doesn't work
        self._instance_meta_data = CollectionModel.MetaDataObj()
        self.document = self.collection_instance.create_document()

        for attribute in self._get_fields():

            attr_val = getattr(self, attribute)
            attr_cls = attr_val.__class__

            if issubclass(attr_cls, ModelField):
                field = copy.deepcopy(attr_val)
                self._instance_meta_data._fields[attribute] = field


    def save(self):
        """
        """

        all_fields = self._instance_meta_data._fields

        for field_name in all_fields:

            local_field = all_fields[field_name]
            is_field_required = local_field.required

            if field_name in self._instance_meta_data._fields:
                # Get field
                field = self._instance_meta_data._fields[field_name]
                # Validate content by field
                field.validate()
                # Get content
                field_value = field.dumps()
            else:
                if not is_field_required:
                    field_value = None
                else:
                    raise CollectionModel.RequiredFieldNoValue()


            self.document.set(key=field_name, value=field_value)

        self.document.save()

    def get_field(self, name):
        """
        """

        return self._instance_meta_data._fields[name]

    def _get_fields(self):
        """
        """

        fields = {}

        for attribute in dir(self):

            attr_val = getattr(self, attribute)
            attr_cls = attr_val.__class__

            if issubclass(attr_cls, ModelField):
                fields[attribute] = attr_val

        return fields

    def __getattribute__(self, item):
        """
        """

        if item == '_instance_meta_data':
            return object.__getattribute__(self, item)

        if item in self._instance_meta_data._fields:
            return self._instance_meta_data._fields[item].get()
        else:
            return super(CollectionModel, self).__getattribute__(item)

    def __setattr__(self, key, value):
        """
        """

        if self._instance_meta_data is None:
            super(CollectionModel, self).__setattr__(key, value)
            return

        if key in self._instance_meta_data._fields:
            self._instance_meta_data._fields[key].set(value)
        else:
            super(CollectionModel, self).__setattr__(key, value)