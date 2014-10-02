Versions
---------

## Current

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

## Future
    
### 0.3
- Index support
- Raw AQL support
- User support
- Batch document insert
- Execute raw ArangoDB queries
- ORM Queryset Filtering (with boolean)
- ORM additional fields:
    - UUID
    - Boolean
    - URL
    - Password

### 0.4
- Index for model fields
- Index queries
- HTTP exception handling
- Document revision

### 0.5
- System
- Replication
- Endpoint
