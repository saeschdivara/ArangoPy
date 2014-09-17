from arangodb.api import SYSTEM_DATABASE, Client
from arangodb.transaction.api import TransactionDatabase
from arangodb.transaction.javascript.code import Generator


class TransactionController(object):
    """
    """

    def start(self, transaction):
        """
        """

        statements = transaction.compile()
        client = Client.instance()
        api = client.api

        try:
            val = api.transaction.post(data={
                'collections': transaction.collections,
                'action': statements,
            })
        except Exception as err:
            print(err.content)


class Transaction(object):
    """
    """

    def __init__(self, collections):
        """
        """

        self.collections = collections
        self.js = Generator()
        self.actions = []

    def database(self, name=SYSTEM_DATABASE):
        """
        """

        return TransactionDatabase(name=name, transaction=self)

    def add_action(self, action):
        self.actions.append(action)

    def compile(self):
        """
        """

        action_statements = ''

        for action in self.actions:
            action_statements += self.js.compile_action(action=action)

        return action_statements