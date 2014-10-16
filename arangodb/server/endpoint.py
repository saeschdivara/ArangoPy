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