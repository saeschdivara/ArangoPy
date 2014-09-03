
class ModelField(object):

    class NotNullableFieldException(Exception):
        """
            Field cannot be null
        """

    def __init__(self, required=True, blank=False, null=True, **kwargs):
        """
        """

        self.required = required
        self.blank = blank
        self.null = null

    def dumps(self):
        """
        """

        return None

    def loads(self, string_val):
        """
        """

        pass

    def validate(self):
        """
        """

        pass

    def set(self, *args, **kwargs):
        """
        """

        pass

    def __unicode__(self):
        return self.dumps()

class CharField(ModelField):

    class TooLongStringException(Exception):
        """
        String is too long
        """

    def __init__(self, max_length=255, **kwargs):
        """
        """

        super(CharField, self).__init__(**kwargs)

        self.max_length = max_length

        if self.null:
            self.text = None
        else:
            self.text = u''

    def dumps(self):
        """
        """

        return self.text

    def loads(self, string_val):
        """
        """

        self.text = string_val

    def validate(self):
        """
        """

        if self.text is None and self.null is False:
            raise CharField.NotNullableFieldException()

        if self.text:
            if len(self.text) > self.max_length:
                raise CharField.TooLongStringException()

    def set(self, *args, **kwargs):
        """
        """

        if len(args) is 1:
            self.text = u'%s' % args[0]