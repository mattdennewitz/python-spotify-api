from spotify_api.models import *

from .lookup import LookupResource
from .search import SearchResource


class SpotifyApi(object):
    """Spotify API facilities
    """

    # search resources
    artists = SearchResource(resource=Artist)
    albums = SearchResource(resource=Album)
    tracks = SearchResource(resource=Track)

    # lookup resource
    lookup = LookupResource()
