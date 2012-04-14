"""
Spotify API wrapper
"""

import requests

from .base import *
from .connection import *
from .fields import *


class ExternalId(Model):
    type = StringField()
    id = StringField()

    def __repr__(self):
        return '<Id: %s / %s>' % (self.type, self.id)


class Availability(Model):
    territories = TerritoryField()


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
    availability = ModelField(Availability)

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

    # mirror of album availability
    availability = ModelField(Availability, object_key='album.availability')

    def __repr__(self):
        return '<Track: %s: %s>' % (
            ', '.join([artist.name for artist in self.artists]),
            self.name)


class MetadataResource(object):

    def __init__(self, resource):
        self.__connection = ApiTransport(resource.resource_name)
        self.resource = resource

    def search(self, query):
        response = self.__connection.get('search', q=query)
        return self.resource.from_response(response.text)


class SpotifyApi(object):
    artists = MetadataResource(resource=Artist)
    albums = MetadataResource(resource=Album)
    tracks = MetadataResource(resource=Track)
