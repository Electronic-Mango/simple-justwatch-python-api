---
icon: lucide/circle-play
---

# Simple JustWatch Python API

!!! warning "Documentation is under active development"
    This documentation is currently under development and might not be fully up-to-date.
    However, the main functionality should be (more or less) correct.

A simple unofficial JustWatch Python API which uses [`GraphQL`](https://graphql.org/)
to access JustWatch data, built with [`httpx`](https://www.python-httpx.org/) and
Python `3.11+`.

This project is managed by [uv](https://docs.astral.sh/uv/).



## Functions

This library provides multiple functions for accessing JustWatch:

 - `search` - search for entries based on title
 - `popular` - get a list of currently popular titles
 - `details` - get details for a title based on its ID
 - `seasons` - get information about all seasons of a show
 - `episodes` - get information about all episodes of a season
 - `offers_for_countries` - get offers for a title based on its ID for multiple
    countries
 - `providers` - get data about all available providers (like Netflix) in a country

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
