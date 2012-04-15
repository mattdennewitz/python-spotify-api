import requests


__all__ = ('ApiTransport', )


from .base import SpotifyException


class ApiTransport(object):

    def __init__(self, resource_name=None, api_version=1):
        self.resource_name = resource_name
        self.api_version = api_version

    def get(self, url, **kwargs):
        response = requests.get(url, params=kwargs)
        if response.status_code != 200:
            raise SpotifyException('<%s> Could not load %s: %s' % (
                    response.status_code, response.url, response.text))
        return response
