---
icon: lucide/tv-minimal-play
---

# Simple JustWatch Python API

A simple *unofficial* JustWatch Python API which uses [`GraphQL`](https://graphql.org/)
to access [JustWatch](https://www.justwatch.com/) data, built with
[`niquests`](https://github.com/jawah/niquests) and available for Python `3.11+`.

This library is published as a
[Python package on PyPi](https://pypi.org/project/simple-justwatch-python-api/).



## Functions

This library provides multiple ways of accessing JustWatch:

 - Search for a title.
 - Get currently popular titles.
 - Get details of a specific entry based on ID.
 - Get information about all seasons of a show.
 - Get information about all episodes of a season.
 - Get offers for a title for multiple countries.
 - Get data about all available providers (such as Netflix) in a country.

All needed functions, data structures, raised exceptions are available through single
module `simplejustwatchapi`.



## Quick example

```python
from simplejustwatchapi import search

results = search("The Matrix", country="US", language="en", count=3)

for entry in results:
    print(entry.title, entry.object_type, len(entry.offers))
```

Examples of parsed [`NamedTuple`][typing.NamedTuple] are in the GitHub repository in
[`examples/`](https://github.com/Electronic-Mango/simple-justwatch-python-api/tree/\
main/examples).



!!! info "Affiliation disclaimer"
    This library is in no way affiliated, associated, authorized, endorsed by, or in any
    way officially connected with JustWatch. This is an independent and unofficial
    project. Use at your own risk.
