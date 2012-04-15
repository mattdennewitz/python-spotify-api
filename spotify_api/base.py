"""
Spotify API resource modeling
"""

import json

from fields import Field


__all__ = ('SpotifyException', 'Model')


class SpotifyException(Exception):
    pass


class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        new_cls = super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)

        if attrs.get('__metaclass__') == ModelMetaclass:
            return new_cls

        fields = {}

        for key, value in attrs.iteritems():
            if isinstance(value, Field):
                if value.field_name is None:
                    value.field_name = key
                fields[key] = value

        new_cls._fields = fields

        return new_cls


class Model(object):
    __metaclass__ = ModelMetaclass

    def __init__(self, **values):
        self._data = {}

        for key in self._fields.keys():
            try:
                setattr(self, key, values.pop(key))
            except AttributeError:
                pass

    @classmethod
    def from_object(cls, obj):
        values = {}

        for field_name, field in cls._fields.items():
            field_key = field.object_key or field_name

            bits = field_key.split('.')
            root_attr = bits.pop(0)
            value = obj.get(root_attr)

            while bits:
                bit = bits.pop(0)

                try:
                    bit = int(bit)
                    value = value[bit]
                except IndexError:
                    value = None
                    break
                except ValueError:
                    if isinstance(value, dict):
                        value = value[bit]
                    else:
                        value = getattr(value, bit, None)
                        if callable(value):
                            value = value()

            if value is not None:
                value = field.to_python(value)
            values[field_name] = value

        return cls(**values)

    @classmethod
    def from_response(cls, obj):
        return cls.from_object(obj)


class Resource(object):

    def _extract_from_response(self, response_body):
        """Unserializes an API response and extracts an object or collection.
        """

        data = json.loads(response_body)
        wrapper_key = self._get_wrapper_key(data)
        return data.get(wrapper_key)

    def _get_wrapper_key(self, data):
        return data['info']['type']
