Versions
---------

## Current

### 0.5
- Bitarray index
- Better traversal query
- (Partly) Extending query as in Django
- ORM index queries
- ORM additional fields:
    - List
    - Dict

## Old

### 0.1
First version which had the following features:

- Some simple queries:
    - Get by example data
    - Random document
    - All documents
- Started with advanced queries
- Started with basic ORM:
    - Models
    - Fields for models (char, number, foreign key)
    - Model query manager
- Transactions to create and update documents
- Managing databases, collections and documents

### 0.2

- More test coverage
- Advanced queries can now be run for multiple collections
- Simple queries added:
    - Remove by example data
    - Update by example data
    - Replace by example data
- ORM:
    - Adding date and datetime fields
    - Queryset for model manager
    
### 0.3
- Index support
- User support
- Execute raw ArangoDB queries
- ORM Queryset Filtering (with boolean)
- ORM Queryset limit
- ORM additional fields:
    - UUID
    - Boolean

### 0.4
- Better code documentation
- Index for model fields
- Index queries
- ORM additional fields:
    - Choice
    - Text
    - ManyToMany

## Future

### 0.6
- Batch execution
- Authentication (done)
- System
- HTTP exception handling
- Document revision (done)
- Model collection prefixes

### 0.7
- Endpoint
- Replication
- Graph
- Through model define