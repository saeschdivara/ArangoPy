class ModelField(object):

    class NotNullableFieldException(Exception):
        """
            Field cannot be null
        """

    class WrongInputTypeException(Exception):
        """
            Field cannot be null
        """

    def __init__(self, required=True, blank=False, null=True, default=None, **kwargs):
        """
        """

        self.required = required
        self.blank = blank
        self.null = null
        self.default = default

        self._model_instance = None

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

    def get(self):
        """
        """

        return self

    def __eq__(self, other):
        """
        """

        return self.__class__ == other.__class__

    def __unicode__(self):
        """
        """

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

        # If null is allowed, default value is None
        if self.null:
            self.text = None
        else:
            # If default value was set
            if self.default:
                self.text = self.default
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
            text = args[0]

            if isinstance(text, basestring):
                self.text = u'%s' % args[0]
            else:
                raise CharField.WrongInputTypeException()

    def __eq__(self, other):
        """
        """

        if super(CharField, self).__eq__(other):
            return self.text == other.text
        else:
            return False


class NumberField(ModelField):

    def __init__(self, **kwargs):
        """
        """

        super(NumberField, self).__init__(**kwargs)


        # If null is allowed, default value is None
        if self.null:
            self.number = None
        else:
            # If default value was set
            if self.default:
                self.number = self.default
            else:
                self.number = 0

    def dumps(self):
        """
        """

        return self.number

    def loads(self, number_val):
        """
        """

        self.number = number_val

    def validate(self):
        """
        """

        if self.number is None and self.null is False:
            raise NumberField.NotNullableFieldException()

        if self.number:
            pass

    def set(self, *args, **kwargs):
        """
        """

        if len(args) is 1:
            number = args[0]

            if isinstance(number, int) or isinstance(number, float):
                self.number = args[0]
            else:
                raise NumberField.WrongInputTypeException()

    def __eq__(self, other):
        """
        """

        if super(NumberField, self).__eq__(other):
            return self.number == other.number
        else:
            return False


class DateField(ModelField):

    def __init__(self, **kwargs):
        """
        """

        super(DateField, self).__init__(**kwargs)

        if self.null:
            self.date = None
        else:
            if self.default:
                self.date = self.default
            else:
                # self.date = Date
                pass


class ForeignKeyField(ModelField):

    def __init__(self, to, **kwargs):
        """
        """

        super(ForeignKeyField, self).__init__(**kwargs)


        # If null is allowed, default value is None
        if self.null:
            self.relation_model = None
        else:
            # If default value was set
            if self.default:
                self.relation_model = self.default
            else:
                self.relation_model = ''

        self.relation_class = to

    def dumps(self):
        """
        """

        return u'%s' % self.relation_model.document

    def loads(self, model_id):
        """
        """

        model = self.relation_class.objects.get(_id=model_id)
        self.relation_model = model

    def validate(self):
        """
        """

        if self.relation_model is None and self.null is False:
            raise NumberField.NotNullableFieldException()

        if self.relation_model:
            pass

    def set(self, *args, **kwargs):
        """
        """

        if len(args) is 1:
            relation_model = args[0]
            self.relation_model = relation_model

    def get(self):
        """
        """

        return self.relation_model

    def __eq__(self, other):
        """
        """

        if super(ForeignKeyField, self).__eq__(other):
            return self.relation_model == other.relation_model
        else:
            return False