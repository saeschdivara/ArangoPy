import timeit
from arangodb.api import Client, Database, Collection


##################################
# These tests
##################################

# Init client
client = Client('localhost')

# Create database in which all collections are created
database_name = 'arangopy_speed_test_database'
try:
    Database.create(database_name)
except:
    client.set_database(database_name)


timer = timeit.default_timer

# Everything needs to be in one try-catch so we can clean up afterwards
try:

    document_number = 10**6 # 1 million
    big_collection_name = 'big_collection'
    big_collection = Collection.create(big_collection_name)

    start = timer()

    for i in range(1, document_number):
        doc = big_collection.create_document()
        doc.index = i
        doc.save()

    elapsed = timer() - start

    print('Adding %s documents to the collection took %s milliseconds' % ( document_number, elapsed) )

    Collection.remove(big_collection_name)

except Exception as err:
    print(err)

# Destroy at the end the database
Database.remove(database_name)