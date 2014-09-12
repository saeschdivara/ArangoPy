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

- Create and destroy databases
- Create and delete collections in specific databases
- Create, update and delete documents in collections
- Use the following simple queries:
-- by-example
-- any
- Use queries where you can set filters and sorting
- ORM
-- Models which have fields:
--- Char field
--- Number field
--- Foreign key field

Usage
------------

## Start with client connection setup
```python

from arangodb.api import Client

client = Client(host='localhost')
```