ArangoPy
========

Python Framework to access https://github.com/triAGENS/ArangoDB


[![Build Status](https://travis-ci.org/saeschdivara/ArangoPy.png?branch=master)](https://travis-ci.org/saeschdivara/ArangoPy)
Coverage Master: [![Coverage Status](https://coveralls.io/repos/saeschdivara/ArangoPy/badge.png?branch=master)](https://coveralls.io/r/saeschdivara/ArangoPy?branch=master)
Coverage Dev: [![Coverage Status](https://img.shields.io/coveralls/saeschdivara/ArangoPy/0.5.svg)](https://coveralls.io/r/saeschdivara/ArangoPy?branch=0.5)
Code Health Master: [![Code Health](https://landscape.io/github/saeschdivara/ArangoPy/master/landscape.png)](https://landscape.io/github/saeschdivara/ArangoPy/master)
Code Health Dev: [![Code Health](https://landscape.io/github/saeschdivara/ArangoPy/0.5/landscape.png)](https://landscape.io/github/saeschdivara/ArangoPy/0.5)
[![Version](https://img.shields.io/pypi/v/ArangoPy.svg)](https://pypi.python.org/pypi/ArangoPy)
[![Downloads](http://img.shields.io/pypi/dm/ArangoPy.svg)](https://pypi.python.org/pypi/ArangoPy)
[![License](https://img.shields.io/pypi/l/ArangoPy.svg)](https://pypi.python.org/pypi/ArangoPy)
[![Build](https://readthedocs.org/projects/arangopy/badge/?version=latest)](https://arangopy.readthedocs.org/en/stable/)


Installation
------------

pip install arangopy

or

python setup.py


Updates
----------
Follow on [Twitter](https://twitter.com/arango_py/)


Supported versions
------------

### ArangoDB

2.2, 2.3, 2.4, 2.5, 2.6

I am running 2.6 at the moment.

### Python

I am testing with Python 2.7 and 3.4


Frameworks integration
-----------------------

Of course, this framework was built to be standing alone but still it has the goal that it can be integrated with
Django. A bridge for this has been started: https://github.com/saeschdivara/ArangoDjango


Features
------------

1. Create and destroy databases
2. Create and delete collections in specific databases
3. Create, update and delete documents in collections
4. Use the following simple queries:
    - by-example
        - get
        - update
        - replace
        - remove
    - any
5. Queries
    - Advanced filtering
    - Sorting
    - Multiple collections
6. ORM
    1. Models which have fields:
        - Boolean field
        - Char field
        - UUID field
        - Number field
        - Date field
        - Datetime field
        - Foreign key field
7. Transactions to create and update documents
8. Index support
9. User support

Usage
------------

## Basic

### Start with client connection setup
```python

from arangodb.api import Client

client = Client(hostname='localhost')
```

### Create database
```python

from arangodb.api import Database

db1 = Database.create(name='test_db')
```

### Create collection
```python

from arangodb.api import Collection

col1 = Collection.create(name='test_collection_nb_1')
```

### Get all collection documents
```python

from arangodb.api import Collection

col1 = Collection.create(name='test_collection_nb_1')

doc1 = col1.create_document()
doc1.extra_value = 'foo -- 123'
doc1.save()

all_docs = col1.documents()
```

## Simple Queries

### Get all documents
```python

from arangodb.api import Collection
from arangodb.query.simple import SimpleQuery

col1 = Collection.create(name='test_collection_nb_1')

doc1 = col1.create_document()
doc1.extra_value = 'foo -- 123'
doc1.save()

doc2 = col1.create_document()
doc2.extra_value = 'aa'
doc2.save()

docs = SimpleQuery.all(collection=col1)
```

### Get by example
```python

from arangodb.api import Collection

col1 = Collection.create(name='test_collection_nb_1')

doc1 = col1.create_document()
doc1.extra_value = 'foo -- 123'
doc1.save()

doc2 = col1.create_document()
doc2.extra_value = 'aa'
doc2.save()

doc = col1.get_document_by_example(example_data={
    'extra_value': doc1.extra_value
})
```

### Get random document
```python

from arangodb.api import Collection
from arangodb.query.simple import SimpleQuery

col1 = Collection.create(name='test_collection_nb_1')

doc1 = col1.create_document()
doc1.extra_value = 'foo -- 123'
doc1.save()

doc2 = col1.create_document()
doc2.extra_value = 'aa'
doc2.save()

doc = SimpleQuery.random(collection=col1)
```

## Advanced Queries

### All documents from a collection
```python

from arangodb.api import Collection
from arangodb.query.advanced import Query

collection_name = 'foo_bar_collection'
col1 = Collection.create(name=collection_name)

q = Query()
q.append_collection(collection_name)
docs = q.execute()
```

### Filtering documents
```python

from arangodb.api import Collection
from arangodb.query.advanced import Query

q = Query()
q.append_collection(self.test_1_col.name)
q.filter(little_number=self.col1_doc3.little_number)

docs = q.execute()

self.assertEqual(len(docs), 1)

doc = docs[0]
self.assertDocumentsEqual(doc, self.col1_doc3)
```

### Filtering documents on multiple collections
```python

from arangodb.api import Collection
from arangodb.query.advanced import Query

q = Query()
q.append_collection(self.test_1_col.name)
q.append_collection(self.test_2_col.name)

dynamic_filter_dict = {}
col_1_filter_name = "%s__%s" % (self.test_1_col.name, "little_number")
col_2_filter_name = "%s__%s" % (self.test_2_col.name, "little_number")

dynamic_filter_dict[col_1_filter_name] = 33
dynamic_filter_dict[col_2_filter_name] = 33
q.filter(bit_operator=Query.OR_BIT_OPERATOR, **dynamic_filter_dict)

docs = q.execute()

self.assertEqual(len(docs), 2)

doc1 = docs[0]
doc2 = docs[1]

self.assertNotEqual(doc1.id, doc2.id)

self.assertEqual(doc1.little_number, 33)
self.assertEqual(doc2.little_number, 33)
```

### Excluding documents from result
```python

from arangodb.api import Collection
from arangodb.query.advanced import Query

q = Query()
q.append_collection(self.test_1_col.name)
q.exclude(loved=False)

docs = q.execute()

self.assertEqual(len(docs), 1)

doc1 = docs[0]

self.assertDocumentsEqual(doc1, self.col1_doc3)
```

### Sorting result
```python

from arangodb.api import Collection
from arangodb.query.advanced import Query

q = Query()
q.append_collection(self.test_1_col.name)
q.order_by('little_number')

docs = q.execute()

self.assertEqual(len(docs), 3)

doc1 = docs[0]
doc2 = docs[1]
doc3 = docs[2]

self.assertDocumentsEqual(doc1, self.col1_doc2)
self.assertDocumentsEqual(doc2, self.col1_doc3)
self.assertDocumentsEqual(doc3, self.col1_doc1)
```

## Transactions

### Create document

```python

from arangodb.query.simple import SimpleQuery
from arangodb.query.utils.document import create_document_from_result_dict
from arangodb.transaction.controller import Transaction, TransactionController

trans = Transaction(collections={
    'write': [
        self.operating_collection,
    ]
})

# Uses already chosen database as usual
collection = trans.collection(name=self.operating_collection)
collection.create_document(data={
    'test': 'foo'
})

ctrl = TransactionController()

transaction_result = ctrl.start(transaction=trans)

transaction_doc = create_document_from_result_dict(transaction_result['result'], self.test_1_col.api)

created_doc = SimpleQuery.get_by_example(self.test_1_col, example_data={
    '_id': transaction_doc.id
})
```

### Update document

```python

from arangodb.transaction.controller import Transaction, TransactionController

doc = self.test_1_col.create_document()
doc.foo = 'bar'
doc.save()

trans = Transaction(collections={
    'write': [
        self.operating_collection,
    ]
})

new_foo_value = 'extra_bar'

collection = trans.collection(self.operating_collection)
collection.update_document(doc_id=doc.id, data={
    'foo': new_foo_value
})

ctrl = TransactionController()
ctrl.start(transaction=trans)

doc.retrieve()

self.assertEqual(doc.foo, new_foo_value)
```

## ORM

### Basic Model
```python

from arangodb.orm.models import CollectionModel
from arangodb.orm.fields import CharField


class TestModel(CollectionModel):

    test_field = CharField(required=True)

# Init collection
TestModel.init()

# Init model
model_1 = TestModel()
model_1.test_field = 'ddd'

# Save model
model_1.save()

all_test_models = TestModel.objects.all()
```

### Foreign key field with Model
```python

from arangodb.orm.models import CollectionModel
from arangodb.orm.fields import CharField, ForeignKeyField


class ForeignTestModel(CollectionModel):

    test_field = CharField(required=True)

class TestModel(CollectionModel):

    other = ForeignKeyField(to=ForeignTestModel, required=True)

# Init collections
ForeignTestModel.init()
TestModel.init()

# Init models
model_1 = ForeignTestModel()
model_1.test_field = 'ddd'

model_2 = TestModel()
model_2.other = model_1

# Save models
model_1.save()
model_2.save()

all_test_models = TestModel.objects.all()
```