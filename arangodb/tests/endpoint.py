import unittest

from arangodb.server.endpoint import Endpoint


class EndpointTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_all_endpoints(self):

        endpoints = Endpoint.all()

        self.assertTrue(len(endpoints) > 0)

        for endpoint in endpoints:
            self.assertTrue('endpoint' in endpoint)
            self.assertTrue('databases' in endpoint)


    # TODO: Take a look at it in the documentation in ArangoDB
    # def test_create_and_delete_endpoint(self):
    #
    #     endpoint_url = 'tcp://127.0.0.1:2211'
    #
    #     Endpoint.create(url=endpoint_url, databases=[])
    #
    #     endpoints = Endpoint.all()
    #
    #     self.assertTrue(len(endpoints) > 1)
    #     print(endpoints)
    #
    #     Endpoint.destroy(url=endpoint_url)