"""
Spotify API fields

Helper fields for easier response parsing.
"""

import decimal


__all__ = ('BooleanField', 'IntegerField', 'StringField', 'DecimalField',
           'ModelField', 'ModelListField', 'TerritoryField')


class Field(object):
    """
    Forms the basis of all field interaction.
    """

    def __get__(self, instance, owner):
        value = instance._data.get(self.field_name)
        return value

    def __set__(self, instance, value):
        instance._data[self.field_name] = value

    def __init__(self, field_name=None, object_key=None):
        self.field_name = field_name
        self.object_key = object_key

    def to_python(self, value):
        return value


class BooleanField(Field):

    def to_python(self, value):
        if not isinstance(value, bool):
            return bool(value)
        return value


class IntegerField(Field):

    def to_python(self, value):
        if not isinstance(value, int):
            return int(value)
        return value


class StringField(Field):

    def to_python(self, value):
        return value.encode('utf-8')


class DecimalField(Field):

    def to_python(self, value):
        if not isinstance(value, basestring):
            value = str(value)
        return decimal.Decimal(value)


class ModelField(Field):

    def __init__(self, model, **kwargs):
        self.model = model
        super(ModelField, self).__init__(**kwargs)

    def to_python(self, value):
        return self.model.from_object(value)


class ModelListField(ModelField):

    def to_python(self, value_list):
        values = []
        for value in value_list:
            values.append(self.model.from_object(value))
        return values


class TerritoryField(Field):
    """
    Special-case field for converting string lists
    of territories into a list representation.
    """

    def to_python(self, value):
        return value.split(' ') if value else []
