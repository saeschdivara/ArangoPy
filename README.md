ArangoPy
========

Python Framework to access https://github.com/triAGENS/ArangoDB


[![Build Status](https://travis-ci.org/saeschdivara/ArangoPy.png?branch=0.1)](https://travis-ci.org/saeschdivara/ArangoPy)
[![Coverage Status](https://img.shields.io/coveralls/saeschdivara/ArangoPy.svg)](https://coveralls.io/r/saeschdivara/ArangoPy?branch=0.1)
[![Version](https://pypip.in/v/ArangoPy/badge.svg)](https://pypi.python.org/pypi/ArangoPy)
[![Downloads](https://pypip.in/d/ArangoPy/badge.svg)](https://pypi.python.org/pypi/ArangoPy)
[![License](https://pypip.in/license/ArangoPy/badge.svg)](https://pypi.python.org/pypi/ArangoPy)


Installation
------------

pip install arangopy

or

python setup.py


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