``python-spotify-api``
======================

A lightweight wrapper around the Spotify metadata API.

This app handles both ``search`` and ``lookup`` endpoints.
Right now, it's considered nearly feature complete,
but will remain "beta" until tests are added.

More info about the Spotify metadata API can be found here:
https://developer.spotify.com/technologies/web-api/.

For issue tracking and feature suggestions, please use the
Github repository: https://github.com/mattdennewitz/python-spotify-api

Here's how it works:

## Installation

For now, install this app via ``pip``:

    pip install -e git+git://github.com/mattdennewitz/python-spotify-api.git

## Usage

This app is very straight-forward to use. To get started,
import and create an instance of the Spotify API:

```python
from spotify_api.api import SpotifyApi

# create api instance
api = SpotifyApi()
```

From here, you can search for artists, albums, and tracks:

```python
# search for artists
results = api.artists.search('drake')
for artist in results:
    print artist.name

# search for albums
results = api.albums.search('take care')
for album in results:
    print album

# search for tracks
results = api.tracks.search('lord knows')
for track in results:
    print track
```

and you can look up metadata given a Spotify URI:

```python
# find album by uri
album = api.lookup.by_id('spotify:album:630o1rKTDsLeIPreOY1jqP')
```

## TODO

The following feature will be added shortly:

- Extended detail support in URI lookup

The following features are under consideration:

- Pagination
- A response metadata object with result counts

