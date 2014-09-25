ArangoPy
========

Python Framework to access https://github.com/triAGENS/ArangoDB


[![Build Status](https://travis-ci.org/saeschdivara/ArangoPy.png?branch=master)](https://travis-ci.org/saeschdivara/ArangoPy)
Master: [![Coverage Status](https://coveralls.io/repos/saeschdivara/ArangoPy/badge.png?branch=master)](https://coveralls.io/r/saeschdivara/ArangoPy?branch=master)
Dev: [![Coverage Status](https://img.shields.io/coveralls/saeschdivara/ArangoPy/0.2.svg)](https://coveralls.io/r/saeschdivara/ArangoPy?branch=0.2)
[![Version](https://pypip.in/v/ArangoPy/badge.svg)](https://pypi.python.org/pypi/ArangoPy)
[![Downloads](http://img.shields.io/pypi/dm/ArangoPy.svg)](https://pypi.python.org/pypi/ArangoPy)
[![License](https://pypip.in/license/ArangoPy/badge.svg)](https://pypi.python.org/pypi/ArangoPy)


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

At the moment I am only testing for ArangoDB 2.2

### Python

At the moment I am only testing for Python 2.7


Features
------------

1. Create and destroy databases
2. Create and delete collections in specific databases
3. Create, update and delete documents in collections
4. Use the following simple queries:
    - by-example
    - any
5. Use queries where you can set filters and sorting
6. ORM
    1. Models which have fields:
        - Char field
        - Number field
        - Foreign key field

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

## Queries

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