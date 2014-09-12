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

## Start with client connection setup
```python

from arangodb.api import Client

client = Client(hostname='localhost')
```