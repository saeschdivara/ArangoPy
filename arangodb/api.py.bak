# -*- coding: utf-8 -*-

import slumber

SYSTEM_DATABASE = '_system'


class Client(object):
    class_instance = None


    def __init__(self, hostname, auth=None, protocol='http', port=8529, database=SYSTEM_DATABASE):
        """
            This should be done only once and sets the instance
        """

        Client.class_instance = self

        self.hostname = hostname
        self.auth = auth
        self.protocol = protocol
        self.port = port
        self.database = database

        self._create_api()

    def set_database(self, name):
        """
        """

        self.database = name
        self._create_api()

    def _create_api(self):

        url = '%s://%s:%s/_db/%s/_api/' % (self.protocol, self.hostname, self.port, self.database)

        self.api = slumber.API(url, auth=self.auth, append_slash=False)

    @classmethod
    def instance(cls, hostname=None, auth=None, protocol=None, port=None, database=None):
        """
            This method is called from everywhere in the code which accesses the database.

            If one of the parameters is set, these variables are overwritten for all others.
        """

        if cls.class_instance is None:
            if hostname is None and auth is None and protocol is None and port is None and database is None:
                cls.class_instance = Client(hostname='localhost')
            else:
                cls.class_instance = Client(hostname=hostname, auth=auth, protocol=protocol, port=port, database=database)
        else:
            if hostname is not None:
                cls.class_instance.hostname = hostname

            if protocol is not None:
                cls.class_instance.hostname = protocol

            if port is not None:
                cls.class_instance.hostname = port

            if database is not None:
                cls.class_instance.database = database

            if auth is not None:
                cls.class_instance.auth = auth

            cls.class_instance._create_api()

        return cls.class_instance

    def collection(self, name):
        """
            Returns a collection with the given name

            :param name Collection name

            :returns Collection
        """

        return Collection(
            name=name,
            api_resource=self.api.collection(name),
            api=self.api,
        )


class Database(object):
    @classmethod
    def create(cls, name, users=None):
        """
            Creates database and sets itself as the active database.

            :param name Database name

            :returns Database
        """

        api = Client.instance().api

        database_data = {
            'name': name,
            'active': True,
        }

        if isinstance(users, list) or isinstance(users, tuple):
            database_data['users'] = users

        data = api.database.post(data=database_data)

        db = Database(
            name=name,
            api=api,
            kwargs=data
        )

        Client.instance().set_database(name=name)

        return db

    @classmethod
    def get_all(cls):
        """
            Returns an array with all databases

            :returns Database list
        """

        api = Client.instance().api

        data = api.database.get()

        database_names = data['result']
        databases = []

        for name in database_names:
            db = Database(name=name, api=api)
            databases.append(db)

        return databases


    @classmethod
    def remove(cls, name):
        """
            Destroys the database.
        """

        client = Client.instance()

        new_current_database = None

        if client.database != name:
            new_current_database = name

        # Deletions are only possible from the system database
        client.set_database(name=SYSTEM_DATABASE)

        api = client.api
        api.database(name).delete()

        if new_current_database:
            client.set_database(name=new_current_database)


    def __init__(self, name, api, **kwargs):
        """
        """

        self.name = name
        self.api = api

    def create_collection(self, name, type=2):
        """
            Shortcut to create a collection

            :param name Collection name
            :param type Collection type (2 = document / 3 = edge)

            :returns Collection
        """

        return Collection.create(name=name, database=self.name, type=type)


class Collection(object):
    @classmethod
    def create(cls, name, database=SYSTEM_DATABASE, type=2):
        """
            Creates collection

            :param name Collection name
            :param database Database name in which it is created
            :param type Collection type (2 = document / 3 = edge)

            :returns Collection
        """

        client = Client.instance()
        api = client.api

        if client.database != database:
            database = client.database

        collection_data = {
            'name': name,
            'type': type,
        }

        data = api.collection.post(data=collection_data)

        collection = Collection(
            name=name,
            database=database,
            api_resource=api.collection,
            api=api,
            kwargs=data
        )

        return collection

    @classmethod
    def get_loaded_collection(cls, name):
        """
        """

        client = Client.instance()
        api = client.api

        data = api.collection(name).properties.get()

        collection = Collection(
            name=name,
            database=client.database,
            api_resource=api.collection,
            api=api,
            kwargs=data
        )

        return collection

    @classmethod
    def remove(cls, name):
        """
            Destroys collection.

            :param name Collection name
        """

        api = Client.instance().api

        api.collection(name).delete()


    def __init__(self, name, api, database=SYSTEM_DATABASE, **kwargs):
        """
        """
        self.name = name
        self.database = database

        self.set_data(**kwargs)

        self.resource = api.collection
        self.api = api

    def set_data(self, **kwargs):
        """
        """

        if 'status' in kwargs:
            self.status = kwargs['status']
        else:
            self.status = 0

        if 'waitForSync' in kwargs:
            self.waitForSync = kwargs['waitForSync']
        else:
            self.waitForSync = False

        if 'isVolatile' in kwargs:
            self.isVolatile = kwargs['isVolatile']
        else:
            self.isVolatile = False

        if 'doCompact' in kwargs:
            self.doCompact = kwargs['doCompact']
        else:
            self.doCompact = None

        if 'journalSize' in kwargs:
            self.journalSize = kwargs['journalSize']
        else:
            self.journalSize = -1

        if 'numberOfShards' in kwargs:
            self.numberOfShards = kwargs['numberOfShards']
        else:
            self.numberOfShards = 0

        if 'shardKeys' in kwargs:
            self.shardKeys = kwargs['shardKeys']
        else:
            self.shardKeys = None

        if 'isSystem' in kwargs:
            self.isSystem = kwargs['isSystem']
        else:
            self.isSystem = False

        if 'type' in kwargs:
            self.type = kwargs['type']
        else:
            self.type = 2

        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            self.id = '0'

    def save(self):
        """
            Updates only waitForSync and journalSize
        """

        data = {
            'waitForSync': self.waitForSync,
            'journalSize': self.journalSize,
        }

        self.resource(self.name).properties.put(data)

    def get(self):
        """
            Retrieves all properties again for the collection and
            sets the attributes.
        """

        data = self.resource(self.name).properties.get()

        self.set_data(**data)

        return data

    def get_figures(self):
        """
            Returns figures about the collection.
        """

        data = self.resource(self.name).figures.get()
        return data['figures']

    def create_document(self):
        """
            Creates a document in the collection.

            :returns Document
        """

        return Document.create(collection=self)

    def create_edge(self, from_doc, to_doc, edge_data={}):
        """
            Creates edge document.

            :param from_doc Document from which the edge comes
            :param to_doc Document to which the edge goes
            :param edge_data Extra data for the edge

            :returns Document
        """

        return Edge.create(
            collection=self,
            from_doc=from_doc,
            to_doc=to_doc,
            edge_data=edge_data
        )

    def documents(self):
        """
            Returns all documents of this collection.

            :returns Document list
        """

        document_list = []
        document_uri_list = self.api.document.get(collection=self.name)['documents']
        for document_uri in document_uri_list:
            splitted_uri = document_uri.split('/')
            document_key = splitted_uri[-1]
            document_id = "%s/%s" % (self.name, document_key)

            doc = Document(
                id=document_id,
                key=document_key,
                collection=self,
                api=self.api
            )

            document_list.append(doc)

        return document_list


class Document(object):
    @classmethod
    def create(cls, collection):
        """
            Creates document object without really creating it in the collection.

            :param collection Collection instance

            :returns Document
        """

        api = Client.instance().api

        doc = Document(
            id='',
            key='',
            collection=collection.name,
            api=api,
        )

        return doc

    def __init__(self, id, key, collection, api, **kwargs):
        """
            :param id Document id (collection_name/number)
            :param key Document key (number)
            :param collection Collection name
            :param api Slumber API object

            :param rev Document revision, default value is key
        """

        self.data = {}
        self.is_loaded = False

        self.id = id
        self.key = key
        self.revision = kwargs.pop('rev', key)
        self.collection = collection
        self.api = api
        self.resource = api.document


    def retrieve(self):
        """
            Retrieves all data for this document and saves it.
        """

        data = self.resource(self.id).get()
        self.data = data

        return data

    def delete(self):
        """
            Removes the document from the collection
        """

        self.resource(self.id).delete()

    def save(self):
        """
            If its internal state is loaded than it will only updated the
            set properties but otherwise it will create a new document.
        """

        # TODO: Add option force_insert

        if not self.is_loaded and self.id is None or self.id == '':
            data = self.resource.post(data=self.data, collection=self.collection)
            self.id = data['_id']
            self.key = data['_key']
            self.revision = data['_rev']
            self.is_loaded = True
        else:
            data = self.resource(self.id).patch(data=self.data)
            self.revision = data['_rev']

    def get(self, key):
        """
            Returns attribute value.

            :param key

            :returns value
        """

        if not self.is_loaded:
            self.retrieve()

            self.is_loaded = True

        if self.has(key=key):
            return self.data[key]
        else:
            return None

    def set(self, key, value):
        """
            Sets document value

            :param key
            :param value
        """

        self.data[key] = value

    def has(self, key):
        """
            Returns if the document has a attribute with the name key
        """

        return key in self.data

    def get_attributes(self):
        """
            Return dict with all attributes
        """

        return self.data

    def __getattr__(self, item):
        """
        """

        val = self.get(key=item)
        return val

    def __setattr__(self, key, value):
        """
        """

        # Set internal variables normally
        if key in ['data', 'is_loaded', 'id', 'key', 'revision', 'collection', 'api', 'resource']:
            super(Document, self).__setattr__(key, value)
        else:
            self.set(key=key, value=value)

    def __repr__(self):
        """
        """
        return self.__str__()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s" % self.id


class Edge(Document):
    @classmethod
    def create(cls, collection, from_doc, to_doc, edge_data={}):
        """
        """

        api = Client.instance().api

        parameters = {
            'collection': collection.name,
            'from': from_doc.id,
            'to': to_doc.id,
        }

        data = api.edge.post(data=edge_data, **parameters)

        doc = Edge(
            id=data['_id'],
            key=data['_key'],
            collection=collection.name,
            api=api,
        )

        return doc

    def __init__(self, id, key, collection, api):
        """
        """

        super(Edge, self).__init__(id=id, key=key, collection=collection, api=api)

        self.resource = api.edge
