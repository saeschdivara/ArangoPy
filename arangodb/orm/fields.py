from datetime import datetime, date


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

class BooleanField(ModelField):

    def __init__(self, **kwargs):
        """
        """

        super(BooleanField, self).__init__(**kwargs)

        # If null is allowed, default value is None
        if self.null and self.default is None:
            self.boolean = None
        else:
            # If default value was set
            if not self.default is None:
                self.boolean = self.default
            else:
                self.boolean = False

    def dumps(self):
        """
        """

        return self.boolean

    def loads(self, boolean_val):
        """
        """

        self.boolean = boolean_val

    def validate(self):
        """
        """

        if self.boolean is None and self.null is False:
            raise BooleanField.NotNullableFieldException()

    def set(self, *args, **kwargs):
        """
        """

        if len(args) is 1:
            boolean = args[0]

            if isinstance(boolean, bool):
                self.boolean = args[0]
            else:
                raise BooleanField.WrongInputTypeException()

    def get(self):
        """
        """

        return self.boolean

    def __eq__(self, other):
        """
        """

        if super(BooleanField, self).__eq__(other):
            return self.boolean == other.boolean
        else:
            return False

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
        if self.null and not self.default:
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

    def get(self):
        """
        """

        return self.text

    def __eq__(self, other):
        """
        """

        if super(CharField, self).__eq__(other):
            return self.text == other.text
        else:
            return False


class UuidField(CharField):

    def __init__(self, max_length=255, **kwargs):
        """
        """

        super(UuidField, self).__init__(**kwargs)

        self.max_length = max_length

        # If null is allowed, default value is None
        if self.null and not self.default:
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
            raise UuidField.NotNullableFieldException()

        if self.text:
            if len(self.text) > self.max_length:
                raise UuidField.TooLongStringException()

    def set(self, *args, **kwargs):
        """
        """

        if len(args) is 1:
            text = args[0]

            if isinstance(text, basestring):
                self.text = u'%s' % args[0]
            else:
                raise UuidField.WrongInputTypeException()

    def get(self):
        """
        """

        return self.text


class NumberField(ModelField):

    def __init__(self, **kwargs):
        """
        """

        super(NumberField, self).__init__(**kwargs)


        # If null is allowed, default value is None
        if self.null and not self.default:
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
                raise NumberField.WrongInputTypeException

    def get(self):
        """
        """

        return self.number

    def __eq__(self, other):
        """
        """

        if super(NumberField, self).__eq__(other):
            return self.number == other.number
        else:
            return False


class DatetimeField(ModelField):

    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, **kwargs):
        """
        """

        super(DatetimeField, self).__init__(**kwargs)

        if self.null and not self.default:
            self.time = None
        else:
            if self.default:
                self.time = self.default
            else:
                self.time = datetime.now()

    def dumps(self):
        """
        """

        return u'%s' % self.time.strftime(DatetimeField.DATE_FORMAT)

    def loads(self, date_string):
        """
        """

        self.time = datetime.strptime(date_string, DatetimeField.DATE_FORMAT)

    def validate(self):
        """
        """

    def set(self, *args, **kwargs):
        """
        """

        if len(args) is 1:
            time = args[0]
            if isinstance(args, basestring):
                self.loads(time)
            else:
                self.time = time

    def get(self):
        """
        """

        return self.time

    def __eq__(self, other):
        """
        """

        if super(DatetimeField, self).__eq__(other):
            return self.time == other.time
        else:
            return False


class DateField(ModelField):

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, **kwargs):
        """
        """

        super(DateField, self).__init__(**kwargs)

        if self.null and not self.default:
            self.date = None
        else:
            if self.default:
                self.date = self.default
            else:
                self.date = date.today()

    def dumps(self):
        """
        """

        return u'%s' % self.date.strftime(DateField.DATE_FORMAT)

    def loads(self, date_string):
        """
        """

        self.date = datetime.strptime(date_string, DateField.DATE_FORMAT)

    def validate(self):
        """
        """

    def set(self, *args, **kwargs):
        """
        """

        if len(args) is 1:
            date = args[0]
            if isinstance(args, basestring):
                self.loads(date)
            else:
                self.date = date

    def get(self):
        """
        """

        return self.date

    def __eq__(self, other):
        """
        """

        if super(DateField, self).__eq__(other):
            return self.date == other.date
        else:
            return False


class ForeignKeyField(ModelField):

    def __init__(self, to, **kwargs):
        """
        """

        super(ForeignKeyField, self).__init__(**kwargs)


        # If null is allowed, default value is None
        if self.null and not self.default:
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
            raise ForeignKeyField.NotNullableFieldException()

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