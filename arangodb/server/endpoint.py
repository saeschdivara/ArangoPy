from arangodb.api import Client


class Endpoint(object):
    """
        Class to manage endpoints on which the server is listening
    """

    @classmethod
    def all(cls):
        """
            Returns a list of all configured endpoints the server is listening on. For each endpoint,
            the list of allowed databases is returned too if set.

            The result is a JSON hash which has the endpoints as keys, and the list of
            mapped database names as values for each endpoint.

            If a list of mapped databases is empty, it means that all databases can be accessed via the endpoint.
            If a list of mapped databases contains more than one database name, this means that any of the
            databases might be accessed via the endpoint, and the first database in the list will be treated
            as the default database for the endpoint. The default database will be used when an incoming request
            does not specify a database name in the request explicitly.

            *Note*: retrieving the list of all endpoints is allowed in the system database only.
            Calling this action in any other database will make the server return an error.
        """

        api = Client.instance().api

        endpoint_list = api.endpoint.get()

        return endpoint_list

    @classmethod
    def create(cls, url, databases):
        """
            If databases is an empty list, all databases present in the server will become accessible via the endpoint,
            with the _system database being the default database.

            If databases is non-empty, only the specified databases will become available via the endpoint.
            The first database name in the databases list will also become the default database for the endpoint.
            The default database will always be used if a request coming in on the endpoint does not specify
            the database name explicitly.

            *Note*: adding or reconfiguring endpoints is allowed in the system database only.
            Calling this action in any other database will make the server return an error.

            Adding SSL endpoints at runtime is only supported if the server was started with SSL
            properly configured (e.g. --server.keyfile must have been set).

            :param url the endpoint specification, e.g. tcp://127.0.0.1:8530
            :param databases a list of database names the endpoint is responsible for.
        """

        api = Client.instance().api

        result = api.endpoint.post(data={
            'endpoint': url,
            'databases': databases,
        })

        return result

    @classmethod
    def destroy(cls, url):
        """
            This operation deletes an existing endpoint from the list of all endpoints,
            and makes the server stop listening on the endpoint.

            *Note*: deleting and disconnecting an endpoint is allowed in the system database only.
            Calling this action in any other database will make the server return an error.

            Futhermore, the last remaining endpoint cannot be deleted as this would make the server kaput.

            :param url The endpoint to delete, e.g. tcp://127.0.0.1:8529.
        """

        api = Client.instance().api

        api.endpoint(url).delete()