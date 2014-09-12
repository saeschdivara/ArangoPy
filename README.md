ArangoPy
========

Python Framework to access https://github.com/triAGENS/ArangoDB


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