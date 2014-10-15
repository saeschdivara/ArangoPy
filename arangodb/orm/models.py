import copy

from arangodb.api import Collection
from arangodb.index.api import Index
from arangodb.index.general import BaseIndex
from arangodb.orm.fields import ModelField
from arangodb.query.advanced import Query, Traveser
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
        # Relations
        self._is_working_on_relations = False
        self._relations_start_model = None
        self._relations_end_model = None
        self._relations_relation_collection = None
        self._related_model_class = None
        # Cache
        self._has_cache = False
        self._cache = []

    def get_field_relations(self, relation_collection, related_model_class, start_model=None, end_model=None):
        """
        """

        self._is_working_on_relations = True
        self._has_cache = False

        self._relations_start_model = start_model
        self._relations_end_model = end_model
        self._relations_relation_collection = relation_collection
        self._related_model_class = related_model_class

        return self

    def all(self):
        """
        """

        self._has_cache = False

        self._query.set_collection(self._collection.name)
        self._query.clear()

    def filter(self, bit_operator=Query.NO_BIT_OPERATOR, **kwargs):
        """
        """

        self._has_cache = False

        self._query.filter(bit_operator=bit_operator, **kwargs)

    def exclude(self, **kwargs):
        """
        """

        self._has_cache = False

        self._query.exclude(**kwargs)

    def limit(self, count, start=-1):
        """
        """

        self._has_cache = False

        self._query.limit(count, start)

    def _clone(self):
        """
        """

        cloned_queryset = CollectionQueryset(manager=self._manager)
        # Query
        cloned_queryset._query = copy.deepcopy(self._query)
        # Relation
        cloned_queryset._is_working_on_relations = self._is_working_on_relations
        cloned_queryset._relations_start_model = self._relations_start_model
        cloned_queryset._relations_end_model = self._relations_end_model
        cloned_queryset._relations_relation_collection = self._is_working_on_relations
        cloned_queryset._related_model_class = self._related_model_class

        return cloned_queryset

    def _generate_cache(self):
        """
        """

        self._cache = [] # TODO: Check how to best clear this list
        self._has_cache = True

        if self._is_working_on_relations:

            start_model = self._relations_start_model
            end_model = self._relations_end_model
            relation_collection = self._relations_relation_collection

            if start_model:
                found_relations = Traveser.follow(
                    start_vertex=start_model.document.id,
                    edge_collection=relation_collection,
                    direction='outbound'
                )
            else:
                found_relations = Traveser.follow(
                    start_vertex=end_model.document.id,
                    edge_collection=relation_collection,
                    direction='inbound'
                )

            result = found_relations
            result_class = self._related_model_class

        else:
            result = self._query.execute()
            result_class = self._manager._model_class

        for doc in result:
            model = self._manager._create_model_from_doc(doc=doc, model_class=result_class)
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

    def _create_model_from_doc(self, doc, model_class=None):
        """
        """

        doc.retrieve()

        attributes = doc.get_attributes()

        model = self._create_model_from_dict(attribute_dict=attributes, model_class=model_class)
        model.document = doc

        return model

    def _create_model_from_dict(self, attribute_dict, model_class=None):
        """
        """

        if model_class:
            model = model_class()
        else:
            model = self._model_class()

        attributes = attribute_dict
        for attribute_name in attributes:

            if not attribute_name.startswith('_'):
                field = model.get_field(name=attribute_name)
                attribute_value = attributes[attribute_name]
                field._model_instance = model
                field.loads(attribute_value)

        return model


class CollectionModel(object):

    collection_instance = None
    collection_name = None

    objects = CollectionModelManager

    _model_meta_data = None
    _instance_meta_data = None

    class RequiredFieldNoValue(Exception):
        """
            Field needs value
        """


    class MetaDataObj(object):

        def __init__(self):
            self._fields = {}

    @classmethod
    def get_collection_fields(cls):
        """
        """

        fields = []

        for attribute in dir(cls):

            attr_val = getattr(cls, attribute)
            attr_cls = attr_val.__class__

            # If it is a model field, call on init
            if issubclass(attr_cls, ModelField):
                fields.append(attr_val)

        model_fields = cls._model_meta_data._fields
        for field_key in  model_fields:
            field = model_fields[field_key]
            fields.append(field)

        return fields

    @classmethod
    def get_model_fields_index(cls):
        """
        """

        index_list = {}

        for attribute in dir(cls):

            attr_val = getattr(cls, attribute)
            attr_cls = attr_val.__class__

            # If it is a model field, call on init
            if issubclass(attr_cls, BaseIndex):
                index_list[attribute] = attr_val

        return index_list

    @classmethod
    def init(cls):
        """
        """

        name = cls.get_collection_name()

        # Set type
        try:
            collection_type = getattr(cls, 'collection_type')
        except:
            collection_type = 2

        # TODO: Database is not set for the collection

        # Create collection
        try:
            cls.collection_instance = Collection.create(name=name, type=collection_type)
        except:
            cls.collection_instance = Collection.get_loaded_collection(name=name)

        try:
            if not isinstance(cls.objects, CollectionModelManager):
                cls.objects = cls.objects(cls)
        except:
            pass # This is the case if init was called more than once

        # Create meta data for collection
        cls._model_meta_data = cls.MetaDataObj()

        # Go through all fields
        for attribute in cls.get_collection_fields():
            # Trigger init event
            attribute.on_init(cls)

        # Go through all index
        model_index_list = cls.get_model_fields_index()
        for index_attribute_name in model_index_list:
            # Save created index
            index_obj = model_index_list[index_attribute_name]
            created_index = Index(collection=cls.collection_instance, index_type_obj=index_obj)
            # Reset class attribute
            setattr(cls, index_attribute_name, created_index)
            # Save index
            created_index.save()

            if not created_index.index_type_obj.is_new:
                created_index.overwrite()

    @classmethod
    def destroy(cls):
        """
        """

        # Go through all fields
        for attribute in cls.get_collection_fields():
            attribute.on_destroy(cls)

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

        fields = self._get_fields()
        for attribute in fields:

            attr_val = fields[attribute]

            # Only attributes which are fields are being copied
            # Copy field with default config
            field = copy.deepcopy(attr_val)
            # Set model instance on the field
            field._model_instance = self
            # Trigger on create so the field knows it
            field.on_create(model_instance=self)
            # Save the new field in the meta data
            self._instance_meta_data._fields[attribute] = field

    def save(self):
        """
        """

        all_fields = self._instance_meta_data._fields

        later_saved_fields = []

        for field_name in all_fields:

            local_field = all_fields[field_name]

            # Check if the field is saved in this collection
            if local_field.__class__.is_saved_in_model:

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

            # This field is saved somewhere else
            else:
                later_saved_fields.append(local_field)

        self.document.save()

        for later_field in later_saved_fields:
            later_field.on_save(self)

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

        model_fields = self.__class__._model_meta_data._fields
        for field_key in  model_fields:
            field = model_fields[field_key]
            fields[field_key] = field

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