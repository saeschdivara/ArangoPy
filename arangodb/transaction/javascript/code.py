from arangodb.transaction.action import DocumentAction


class Generator(object):
    """
    """

    def __init__(self):
        """
        """

        self.statements = ''
        self.last_variable_name = ''
        self.document_variable_counter = 1
        self.has_db_defined = False

    def compile_action(self, action):
        """
        """

        if not self.has_db_defined:
            self.statements += "var db = require('internal').db;"

        if isinstance(action, DocumentAction):

            if action.action_type == 'create':
                doc_var_name = self._get_next_document_variable_name()
                self.statements += '%s = db.%s.save(%s);' % (
                    doc_var_name,
                    action.collection_name,
                    action.document_data
                )

            elif action.action_type == 'update':
                self.statements += 'db.%s.update("%s", %s);' % (
                    action.collection_name,
                    action._id,
                    action.document_data
                )

    def code(self):
        """
        """

        return 'function() { %s return %s; }' % ( self.statements, self.last_variable_name )

    def _get_next_document_variable_name(self):
        next_name = "doc_var_%s" % self.document_variable_counter

        self.document_variable_counter += 1
        self.last_variable_name = next_name

        return next_name