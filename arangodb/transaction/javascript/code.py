from arangodb.transaction.action import DocumentAction


class Generator(object):
    """
    """

    def __init__(self):
        """
        """

        self.statements = ''
        self.has_db_defined = False

    def compile_action(self, action):
        """
        """

        if not self.has_db_defined:
            self.statements += "var db = require('internal').db;"

        if isinstance(action, DocumentAction):

            self.statements += 'db.%s.save(%s);' % (
                action.collection_name,
                action.document_data
            )

    def code(self):
        """
        """

        return 'function() { %s }' % self.statements