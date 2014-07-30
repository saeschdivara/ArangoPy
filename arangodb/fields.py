
class ModelField(object):

    def __init__(self, is_required=True, **kwargs):
        """
        """

        self.is_required = is_required

    def dumps(self):
        """
        """

        return u''

    def loads(self, string_val):
        """
        """

        pass

    def set(self, *args, **kwargs):
        """
        """

        pass

    def contribute_to_model(self, model):
        """
        """

        #

class TextField(ModelField):

    def __init__(self, is_required=True, **kwargs):
        """
        """

        super(TextField, self).__init__(**kwargs)

        self.text = u''

    def dumps(self):
        """
        """

        return u'%s' % self.text

    def loads(self, string_val):
        """
        """

        self.text = string_val

    def set(self, *args, **kwargs):
        """
        """

        if len(args) is 1:
            self.text = args[0]