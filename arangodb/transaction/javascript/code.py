from arangodb.transaction.action import CollectionAction


class Generator(object):
    """
    """

    def __init__(self):
        """
        """

    def compile_action(self, action):
        """
        """

        if isinstance(action, CollectionAction):
            return 'db._useDatabase("%s");db._create("%s");' % (
                action.database, action.name
            )