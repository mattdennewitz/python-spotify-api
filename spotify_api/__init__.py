"""Spotify API wrapper
"""

import decimal
import json

import requests


class SpotifyException(Exception):
    pass


class Field(object):

    def __init__(self, field_name=None, object_key=None):
        self.field_name = field_name
        self.object_key = object_key

    def __get__(self, instance, owner):
        value = instance._data.get(self.field_name)
        return value

    def __set__(self, instance, value):
        instance._data[self.field_name] = value


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
            value = obj.get(field_key)
            if value is not None:
                value = field.to_python(value)
            values[field_name] = value

        return cls(**values)

    @classmethod
    def from_response(cls, data):
        data = json.loads(data)

        objects = data.get(cls.wrapper)

        for obj in objects:
            yield cls.from_object(obj)


class ExternalId(Model):
    type = StringField()
    id = StringField()

    def __repr__(self):
        return '<Id: %s / %s>' % (self.type, self.id)


class Artist(Model):
    resource_name = 'artist'
    wrapper = 'artists'

    name = StringField()
    href = StringField()
    popularity = DecimalField()

    def __repr__(self):
        return '<Artist: %s>' % self.name


class Album(Model):
    resource_name = 'album'
    wrapper = 'albums'

    artists = ModelListField(Artist)
    artist_id = StringField(object_key='artist-id')
    external_ids = ModelListField(ExternalId, object_key='external-ids')
    name = StringField()
    href = StringField()
    popularity = DecimalField()
    released = IntegerField()

    def __repr__(self):
        return '<Album: %s: %s>' % (
            ', '.join([artist.name for artist in self.artists]),
            self.name)


class Track(Model):
    resource_name = 'track'
    wrapper = 'tracks'

    artists = ModelListField(Artist)
    album = ModelField(Album)
    external_ids = ModelListField(ExternalId, object_key='external-ids')
    name = StringField()
    popularity = DecimalField()
    href = StringField()
    length = DecimalField()
    track_number = IntegerField(object_key='track-number')
    available = BooleanField()
    disc_number = IntegerField(object_key='disc-number')

    def __repr__(self):
        return '<Track: %s: %s>' % (
            ', '.join([artist.name for artist in self.artists]),
            self.name)


class MetadataResource(object):
    METHODS = ('search', 'lookup')

    def __init__(self, resource, api_version=1):
        self.resource = resource
        self.api_version = api_version

    def __get_url(self, method):
        return 'http://ws.spotify.com/%(method)s/%(version)s/%(resource)s.json' % {
            'method': method,
            'version': self.api_version,
            'resource': self.resource.resource_name}

    def __make_request(self, method, **kwargs):
        response = requests.get(self.__get_url(method), params=kwargs)
        if response.status_code != 200:
            raise SpotifyException('<%s> Could not load %s: %s' % (
                    response.status_code, response.url, response.text))
        return response

    def search(self, query):
        response = self.__make_request('search', q=query)
        return self.resource.from_response(response.text)

    def lookup(self, query, extra):
        response = self.__make_request('lookup', q=query, extras=extra)
        return self.resource.from_response(response.text)


class SpotifyApi(object):
    artists = MetadataResource(resource=Artist)
    albums = MetadataResource(resource=Album)
    tracks = MetadataResource(resource=Track)
