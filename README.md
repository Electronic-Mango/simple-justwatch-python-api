# Simple JustWatch Python API

[![PyPi](https://img.shields.io/pypi/v/simple-justwatch-python-api.svg)](https://pypi.python.org/pypi/simple-justwatch-python-api)
[![License](https://img.shields.io/pypi/l/simple-justwatch-python-api.svg)](https://pypi.python.org/pypi/simple-justwatch-python-api)
[![Python versions](https://img.shields.io/pypi/pyversions/simple-justwatch-python-api.svg)](https://pypi.python.org/pypi/simple-justwatch-python-api)
[![CodeQL](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql.yml)
[![Ruff](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/ruff.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/ruff.yml)
[![Pytest](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml)
[![Coverage Status](https://coveralls.io/repos/github/Electronic-Mango/simple-justwatch-python-api/badge.svg?branch=main)](https://coveralls.io/github/Electronic-Mango/simple-justwatch-python-api?branch=main)

A simple unofficial JustWatch Python API which uses [`GraphQL`](https://graphql.org/)
to access JustWatch data, available for Python `3.11+`.

This project is managed by [uv](https://docs.astral.sh/uv/).



## Installation

This library is available through
[PyPi](https://pypi.org/project/simple-justwatch-python-api/):
```bash
pip install simple-justwatch-python-api
```


## Documentation

Detailed documentation is available at:
<https://electronic-mango.github.io/simple-justwatch-python-api/>.



## Highlights

This Python library has multiple functions:

 - `search` - search for entries based on title
 - `popular` - get a list of currently popular titles
 - `details` - get details for entry based on its node ID
 - `seasons` - get information about all seasons of a show
 - `episodes` - get information about all episodes of a season
 - `offers_for_countries` - get offers for entry based on its node ID, can look for
    offers in multiple countries
 - `providers` - get data about available providers (e.g., Netflix)

Example outputs from all functions are in
[`examples/`](https://github.com/Electronic-Mango/simple-justwatch-python-api/tree/main/examples).



## Quick example

```python
from simplejustwatchapi import search

results = search("The Matrix", country="US", language="en", count=3)

for entry in results:
    print(entry.title, entry.object_type, len(entry.offers))
```


## License

This library is licensed under **MIT license** (
[LICENSE](https://github.com/Electronic-Mango/simple-justwatch-python-api/blob/main/LICENSE)
or <https://opensource.org/license/MIT>).



## Disclaimer

This library is in no way affiliated, associated, authorized, endorsed by, or in any way
officially connected with JustWatch. This is an independent and unofficial project.

Use at your own risk.
