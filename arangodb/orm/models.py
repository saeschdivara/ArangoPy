import copy

from arangodb.api import Collection
from arangodb.index.api import Index
from arangodb.index.general import BaseIndex
from arangodb.orm.fields import ModelField
from arangodb.query.advanced import Query, Traveser
from arangodb.query.simple import SimpleQuery, SimpleIndexQuery


class LazyQueryset(object):
    """
    """

    def __init__(self, manager):
        """
        """

        self._manager = manager
        self._collection = manager._model_class.collection_instance

        # Cache
        self._has_cache = False
        self._cache = []

    def count(self):
        """
        """

        if not self._has_cache:
            self._generate_cache()

        return len(self._cache)

    def _generate_cache(self):
        """
        """

        self._cache = [] # TODO: Check how to best clear this list
        self._has_cache = True

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

        return self.count()


class IndexQueryset(LazyQueryset):
    """
    """

    def __init__(self, manager):
        """
        """

        super(IndexQueryset, self).__init__(manager=manager)

        self._index = None
        self._filters = {}

    def set_index(self, index):
        """
        """

        self._has_cache = False

        self._index = index

    def filter(self, **kwargs):
        """
        """

        self._has_cache = False

        for arg_name, arg_value in kwargs.items():
            self._filters[arg_name] = arg_value

        return self

    def _generate_cache(self):
        """
        """

        super(IndexQueryset, self)._generate_cache()

        index_field = getattr(self._manager._model_class, self._index)
        result = None

        # All have these attributes
        if 'skip' in self._filters:
            skip = self._filters['skip']
        else:
            skip = None

        if 'limit' in self._filters:
            limit = self._filters['limit']
        else:
            limit = None

        # Hash index
        if index_field.index_type_obj.type_name == 'hash':

            result = SimpleIndexQuery.get_by_example_hash(
                collection=index_field.collection,
                index_id=index_field.index_type_obj.id,
                example_data=self._filters,
                allow_multiple=True,
                skip=skip,
                limit=limit,
            )

        # Skiplist index
        if index_field.index_type_obj.type_name == 'skiplist':

            range_query = 'left' in self._filters
            range_query = range_query and 'right' in self._filters
            range_query = range_query and 'closed' in self._filters
            range_query = range_query and 'attribute' in self._filters

            # Range query
            if range_query:
                result = SimpleIndexQuery.range(
                    collection=index_field.collection,
                    index_id=index_field.index_type_obj.id,
                    attribute=self._filters['attribute'],
                    left=self._filters['left'],
                    right=self._filters['right'],
                    closed=self._filters['closed'],
                    skip=skip,
                    limit=limit,
                )

            # Normal search query
            else:
                result = SimpleIndexQuery.get_by_example_skiplist(
                    collection=index_field.collection,
                    index_id=index_field.index_type_obj.id,
                    example_data=self._filters,
                    allow_multiple=True,
                    skip=skip,
                    limit=limit,
                )

        # Fulltext index
        if index_field.index_type_obj.type_name == 'fulltext':

            result = SimpleIndexQuery.fulltext(
                collection=index_field.collection,
                index_id=index_field.index_type_obj.id,
                attribute=self._filters['attribute'],
                example_text=self._filters['example_text'],
                skip=skip,
                limit=limit,
            )

        # Cap constraint
        if index_field.index_type_obj.type_name == 'cap':
            pass

        # Geo index
        if index_field.index_type_obj.type_name == 'geo':

            if 'radius' in self._filters:
                result = SimpleIndexQuery.within(
                    collection=index_field.collection,
                    index_id=index_field.index_type_obj.id,
                    latitude=self._filters['latitude'],
                    longitude=self._filters['longitude'],
                    radius=self._filters['radius'],
                    distance=self._filters['distance'],
                    skip=skip,
                    limit=limit,
                )
            else:
                result = SimpleIndexQuery.near(
                    collection=index_field.collection,
                    index_id=index_field.index_type_obj.id,
                    latitude=self._filters['latitude'],
                    longitude=self._filters['longitude'],
                    distance=self._filters['distance'],
                    skip=skip,
                    limit=limit,
                )

        # Save cache
        if isinstance(result, list):
            self._cache = result
        else:
            self._cache.append(result)


class CollectionQueryset(LazyQueryset):
    """
    """

    def __init__(self, manager):
        """
        """

        super(CollectionQueryset, self).__init__(manager=manager)

        self._query = Query()
        # Relations
        self._is_working_on_relations = False
        self._relations_start_model = None
        self._relations_end_model = None
        self._relations_relation_collection = None
        self._related_model_class = None

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

    def get(self, **kwargs):
        """
        """

        return self._manager.get(**kwargs)

    def all(self):
        """
        """

        self._has_cache = False

        self._query.set_collection(self._collection.name)
        self._query.clear()

        return self

    def filter(self, bit_operator=Query.NO_BIT_OPERATOR, **kwargs):
        """
        """

        self._has_cache = False

        kwargs = self._normalize_kwargs(**kwargs)
        self._query.filter(bit_operator=bit_operator, **kwargs)

        return self

    def exclude(self, **kwargs):
        """
        """

        self._has_cache = False

        kwargs = self._normalize_kwargs(**kwargs)
        self._query.exclude(**kwargs)

        return self

    def limit(self, count, start=-1):
        """
        """

        self._has_cache = False

        self._query.limit(count, start)

        return self

    def order_by(self, field, order):
        """
        """

        self._has_cache = False

        self._query.order_by(field=field, order=order)

        return self

    def _normalize_kwargs(self, **kwargs):
        """
        """

        # You can use this way models
        for key, value in kwargs.items():
            if isinstance(value, CollectionModel):
                kwargs[key] = value.id

        return kwargs

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

        super(CollectionQueryset, self)._generate_cache()

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

class CollectionModelManager(object):

    queryset = CollectionQueryset

    def __init__(self, cls):
        """
        """

        self._model_class = cls

    def get(self, **kwargs):
        """
        """

        collection = self._model_class.collection_instance

        kwargs = self._normalize_kwargs(**kwargs)

        doc = SimpleQuery.get_by_example(collection=collection, example_data=kwargs)

        if doc is None:
            return None

        model = self._create_model_from_doc(doc=doc)

        return model

    def get_or_create(self, **kwargs):
        """
            Looks up an object with the given kwargs, creating one if necessary.
            Returns a tuple of (object, created), where created is a boolean
            specifying whether an object was created.
        """

        model = self.get(**kwargs)

        is_created = False

        if model is None:
            is_created = True
            model = self._model_class()

            for key, value in kwargs.items():
                setattr(model, key, value)

        return model, is_created

    def all(self):
        """
        """

        queryset = self.queryset(manager=self)
        return queryset.all()

    def filter(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        queryset = self.queryset(manager=self)
        kwargs = self._normalize_kwargs(**kwargs)

        return queryset.all().filter(**kwargs)

    def exclude(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        queryset = self.queryset(manager=self)
        kwargs = self._normalize_kwargs(**kwargs)

        return queryset.all().exclude(**kwargs)

    def limit(self, count, start=-1):
        """

        :return:
        """

        queryset = self.queryset(manager=self)
        return queryset.all().limit(count=count, start=start)

    def search_by_index(self, index, **kwargs):
        """
        """

        queryset = IndexQueryset(manager=self)
        queryset.set_index(index=index)
        kwargs = self._normalize_kwargs(**kwargs)

        return queryset.filter(**kwargs)

    def search_in_range(self, index, attribute, left, right, closed, **kwargs):
        """
        """

        queryset = IndexQueryset(manager=self)
        queryset.set_index(index=index)

        kwargs['attribute'] = attribute
        kwargs['left'] = left
        kwargs['right'] = right
        kwargs['closed'] = closed

        return queryset.filter(**kwargs)

    def search_fulltext(self, index, attribute, example_text, **kwargs):
        """
        """

        queryset = IndexQueryset(manager=self)
        queryset.set_index(index=index)

        kwargs['attribute'] = attribute
        kwargs['example_text'] = example_text

        kwargs = self._normalize_kwargs(**kwargs)

        return queryset.filter(**kwargs)

    def search_near(self, index, latitude, longitude, distance=None, **kwargs):
        """
        """

        queryset = IndexQueryset(manager=self)
        queryset.set_index(index=index)

        kwargs['latitude'] = latitude
        kwargs['longitude'] = longitude
        kwargs['distance'] = distance

        kwargs = self._normalize_kwargs(**kwargs)

        return queryset.filter(**kwargs)

    def search_within(self, index, latitude, longitude, radius, distance=None, **kwargs):
        """
        """

        queryset = IndexQueryset(manager=self)
        queryset.set_index(index=index)

        kwargs['latitude'] = latitude
        kwargs['longitude'] = longitude
        kwargs['radius'] = radius
        kwargs['distance'] = distance

        kwargs = self._normalize_kwargs(**kwargs)

        return queryset.filter(**kwargs)

    def _normalize_kwargs(self, **kwargs):
        """
        """

        # You can use this way models
        for key, value in kwargs.items():
            if isinstance(value, CollectionModel):
                kwargs[key] = value.id

        return kwargs

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
    def get_all_fields(cls, class_obj=None, fields=None):
        """
            TODO: This needs to be properly used
        """

        def return_fields(obj):

            internal_fields = fields
            if internal_fields is None:
                internal_fields = {}

            for attribute in dir(obj):

                try:
                    attr_val = getattr(obj, attribute)
                    attr_cls = attr_val.__class__

                    # If it is a model field, call on init
                    if issubclass(attr_cls, ModelField):
                        internal_fields[attribute] = attr_val
                except:
                    pass

            return internal_fields

        if class_obj is None:
            class_obj = cls

            fields = return_fields(class_obj)
            for parent_class in cls.__bases__:
                parent_fields = cls.get_all_fields(parent_class, fields)
                for field_name, field_value in parent_fields.items():
                    if not field_name in fields:
                        fields[field_name] = field_value

            return fields

        else:
            if not isinstance(class_obj, CollectionModel):
                return fields


    @classmethod
    def get_collection_fields_dict(cls):
        """
        """

        fields = {}

        for attribute in dir(cls):

            try:
                attr_val = getattr(cls, attribute)
                attr_cls = attr_val.__class__

                # If it is a model field, call on init
                if issubclass(attr_cls, ModelField):
                    fields[attribute] = attr_val
            except:
                pass

        model_fields = cls._model_meta_data._fields
        for field_key in  model_fields:
            field = model_fields[field_key]
            fields[field_key] = field

        return fields

    @classmethod
    def get_collection_fields(cls):
        """
        """

        fields = []

        for attribute in dir(cls):

            try:
                attr_val = getattr(cls, attribute)
                attr_cls = attr_val.__class__

                # If it is a model field, call on init
                if issubclass(attr_cls, ModelField):
                    fields.append(attr_val)
            except:
                pass

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

            try:
                attr_val = getattr(cls, attribute)
                attr_cls = attr_val.__class__

                # If it is a model field, call on init
                if issubclass(attr_cls, BaseIndex):
                    index_list[attribute] = attr_val

            except:
                pass

        return index_list

    @classmethod
    def init(cls):
        """
        """

        # TODO: Deal with super classes

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

        cls._default_manager = cls.objects

        # Create meta data for collection
        cls._model_meta_data = cls.MetaDataObj()

        if hasattr(cls, 'Meta'):
            cls._meta = cls.Meta()
            cls._meta.model_name = name
            cls._meta.object_name = name

            # Giving other classes the chance to extend the meta data on init
            if hasattr(cls, 'extend_meta_data'):
                cls.extend_meta_data(cls, cls._meta)

        # Go through all fields
        fields_dict = cls.get_collection_fields_dict()
        for attribute_name in fields_dict:
            attribute = fields_dict[attribute_name]
            # Trigger init event
            attribute.on_init(cls, attribute_name)

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

                    # Read only fields are ignored
                    if field.read_only:
                        continue

                    # If the fields needs to do something before the save
                    field.on_save(self)

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

        if name == 'id':
            return self.document.id
        elif name == 'key':
            return self.document.key

        return self._instance_meta_data._fields[name]

    def _get_fields(self):
        """
        """

        fields = {}

        for attribute in dir(self):

            try:
                attr_val = getattr(self, attribute)
                attr_cls = attr_val.__class__

                if issubclass(attr_cls, ModelField):
                    fields[attribute] = attr_val
            except:
                pass

        model_fields = self.__class__._model_meta_data._fields
        for field_key in  model_fields:
            field = model_fields[field_key]
            fields[field_key] = field

        return fields

    def serializable_value(self, attr):
        """
        """

        return getattr(self, attr)

    def __getattribute__(self, item):
        """
        """

        if item == '_instance_meta_data':
            return object.__getattribute__(self, item)

        if item in self._instance_meta_data._fields:
            return self._instance_meta_data._fields[item].get()
        elif item == 'id':
            return self.document.id
        elif item == 'key' or item == 'pk':
            return self.document.key
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