import logging
from slumber.exceptions import HttpClientError
from arangodb.api import Client
from arangodb.transaction.api import TransactionCollection
from arangodb.transaction.javascript.code import Generator


logger = logging.getLogger(name='ArangoPy')

class TransactionController(object):
    """
    """

    class InvalidTransactionException(Exception):
        """
        """

    def start(self, transaction):
        """
        """

        statements = transaction.compile()
        client = Client.instance()
        api = client.api

        query = {
            'collections': transaction.collections,
            'action': statements,
        }

        logger.debug(query)

        try:
            val = api.transaction.post(data=query)
            return val
        except HttpClientError as err:
            raise TransactionController.InvalidTransactionException(err.content)


class Transaction(object):
    """
    """

    def __init__(self, collections):
        """
        """

        self.collections = collections
        self.js = Generator()
        self.actions = []

    def collection(self, name):
        """
        """

        return TransactionCollection(name=name, transaction=self)

    def add_action(self, action):
        self.actions.append(action)

    def compile(self):
        """
        """

        for action in self.actions:
            self.js.compile_action(action=action)

        return self.js.code()