import requests

from .base import SpotifyException


__all__ = ('ApiTransport', )


class ApiTransport(object):
    """Handles the request/response dirty work.
    """

    @classmethod
    def get(cls, url, **kwargs):
        response = requests.get(url, params=kwargs)
        if response.status_code != 200:
            raise SpotifyException('<%s> Could not load %s: %s' % (
                    response.status_code, response.url, response.text))
        return response
