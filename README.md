# Simple JustWatch Python API

[![CodeQL](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql-analysis.yml)
[![Black](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/flake8.yml)
[![isort](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/isort.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/isort.yml)
[![Pytest](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml)
[![Coverage Status](https://coveralls.io/repos/github/Electronic-Mango/simple-justwatch-python-api/badge.svg?branch=main)](https://coveralls.io/github/Electronic-Mango/simple-justwatch-python-api?branch=main)
[![PyPI - Version](https://img.shields.io/pypi/v/simple-justwatch-python-api)](https://pypi.org/project/simple-justwatch-python-api/)

A simple unofficial JustWatch Python API which uses [`GraphQL`](https://graphql.org/) to access JustWatch data, built with [`httpx`](https://www.python-httpx.org/) and `Python3.11`.



## Installation

Project is available in [PyPi](https://pypi.org/project/simple-justwatch-python-api/):
```bash
pip install simple-justwatch-python-api
```



## Usage

Currently, there's only one function available - search JustWatch:
```python
from simplejustwatchapi.justwatch import search

results = search("title", "US", "en", 5, True)
```

Only the first argument is required, it specifies a title to search.

Other arguments in order are:
1. `str` country code to search for offers, have to be a 2-letter code, e.g. `US`, `GB`, `FR`, etc.
It should be uppercase, however lowercase codes are automatically converted to uppercase. By default `US` is used.
2. `str` language code, usually 2-letter lowercase code, e.g. `en`, `fr`, etc. By default `en` is used.
3. `int` how many results should be returned. Actual response can contain fewer entries if fewer are found.
By default `4` is used.
4. `bool` specify if only best offers should be returned (`True`) or all offers (`False`).
By default `True` is used.

Returned value is a list of `MediaEntry` objects:
```python
class MediaEntry(NamedTuple):
    entry_id: str
    object_id: int
    object_type: str
    title: str
    url: str
    release_year: int
    release_date: str
    genres: list[str]
    imdb_id: str | None
    poster: str
    backdrops: list[str]
    offers: list[Offer]

class Offer(NamedTuple):
    monetization_type: str
    presentation_type: str
    url: str
    price_string: str | None
    price_value: float | None
    price_currency: str
    name: str
    technical_name: str
    icon: str
```



## Disclaimer

This API is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with JustWatch.
This is an independent and unofficial project.
Use at your own risk.
