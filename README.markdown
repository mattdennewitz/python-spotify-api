Spotify Metadata Search Wrapper
===============================

Quick pass at wrapping the Spotify metadata search API.
API results are *kind of* consistent, but not totally.

Usage
-----

```python
from spotify_api import SpotifyApi

# create api instance
api = SpotifyApi()

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

TODO
----

- Slicing
- Real results object with totals and results metadata
