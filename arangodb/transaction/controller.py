from arangodb.api import SYSTEM_DATABASE
from arangodb.transaction.api import TransactionDatabase
from arangodb.transaction.javascript.code import Generator


class TransactionController(object):
    """
    """

    def start(self, transaction):
        """
        """

        transaction.compile()


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

        for action in self.actions:
            print(self.js.compile_action(action=action))