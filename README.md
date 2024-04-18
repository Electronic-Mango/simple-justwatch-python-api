# Simple JustWatch Python API

[![CodeQL](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql-analysis.yml)
[![Black](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/flake8.yml)
[![isort](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/isort.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/isort.yml)
[![Pytest](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml)
[![Coverage Status](https://coveralls.io/repos/github/Electronic-Mango/simple-justwatch-python-api/badge.svg?branch=main)](https://coveralls.io/github/Electronic-Mango/simple-justwatch-python-api?branch=main)
[![PyPI - Version](https://img.shields.io/pypi/v/simple-justwatch-python-api)](https://pypi.org/project/simple-justwatch-python-api/)

A simple unofficial JustWatch Python API which uses [`GraphQL`](https://graphql.org/) to access JustWatch data, built with [`httpx`](https://www.python-httpx.org/) and `Python3.11`.



## Table of contents

* [Installation](#installation)
* [Usage](#usage)
  * [Search](#search)
  * [Details](#details)
  * [Offers for countries](#offers-for-countries)
* [Return data structures](#return-data-structures)
* [Locale, language, country](#locale-language-country)
* [Disclaimer](#disclaimer)


## Installation

Project is available in [PyPi](https://pypi.org/project/simple-justwatch-python-api/):
```bash
pip install simple-justwatch-python-api
```



## Usage

This Python API has 3 functions:

 - `search` - search for entries based on title
 - `details` - get details for entry based on its node ID
 - `offers_for_countries` - get offers for entry based on its node ID, can look for offers
   in multiple countries

Detailed documentation is available in https://electronic-mango.github.io/simple-justwatch-python-api/.

Example outputs from all commands are in [`examples/`](examples/) directory.


### Search
Search functions allows for searching entries based on a given title.

```python
from simplejustwatchapi.justwatch import search

results = search("title", "US", "en", 5, True)
```

Only the first argument is required, it specifies a title to search.

|   | Argument    | Type   | Required | Default value | Description                                            |
|---|-------------|--------|----------|---------------|--------------------------------------------------------|
| 1 | `title`     | `str`  | **YES**  | -             | Title to look up                                       |
| 2 | `country`   | `str`  | NO       | `"US"`        | Country to search for offers                           |
| 3 | `language`  | `str`  | NO       | `"en"`        | Language of responses                                  |
| 4 | `count`     | `int`  | NO       | `4`           | Up to how many entries should be returned              |
| 5 | `best_only` | `bool` | NO       | `True`        | Determines whether only best offers should be returned |

`country` must be **ISO 3166-1 alpha-2** 2-letter code , e.g. `US`, `GB`, `FR`.
It should be uppercase, however lowercase codes are automatically converted to uppercase.

`language` is a **ISO 639-1** (usually) 2-letter code, lowercase, e.g. `en`, `fr`.

`count` determines **up to** how many entries should be returned.
If JustWatch GraphQL API returns fewer entries, then this function will also return fewer values.

`best_only` determines whether similar offers, but lower quality should be included in response.
If a platform offers streaming for a given entry in 4K, HD and SD, then `best_only = True` will return only the 4K offer, `best_only = False` will return all three.

Returned value is a list of [`MediaEntry`](#return-data-structures) objects.

Example command and its output is in [`examples/search_output.py`](examples/search_output.py).


### Details

Details function allows for looking up details for a single entry via its node ID.
Node ID can be taken from output of the [`search`](#search) command.

Output from this function contains the same data as a single entry from the [`search`](#search) command.
There's no reason to first use the [`search`](#search) command, then use node ID from one of entries for this command.

```python
from simplejustwatchapi.justwatch import details

results = details("nodeID", "US", "en", False)
```

Only the first argument is required - the node ID of element to look up details for.

|   | Argument    | Type   | Required | Default value | Description                                            |
|---|-------------|--------|----------|---------------|--------------------------------------------------------|
| 1 | `node_id`   | `str`  | **YES**  | -             | Node ID to look up                                     |
| 2 | `country`   | `str`  | NO       | `"US"`        | Country to search for offers                           |
| 3 | `language`  | `str`  | NO       | `"en"`        | Language of responses                                  |
| 5 | `best_only` | `bool` | NO       | `True`        | Determines whether only best offers should be returned |

General usage of these arguments matches the [`search`](#search) command.

Returned value is a single [`MediaEntry`](#return-data-structures) object.

Example command and its output is in [`examples/details_output.py`](examples/details_output.py).


### Offers for countries

This function allows looking up offers for entry by given node ID.
It allows specifying a set of countries, instead of a single one.
This way you can simultaneously look up offers for multiple countries.

```python
from simplejustwatchapi.justwatch import offers_for_countries

results = offers_for_countries("nodeID", {"US", "UK", "CA"}, "en", True)
```

First two arguments are required - node ID, and set of countries.

|   | Argument    | Type       | Required | Default value | Description                                            |
|---|-------------|------------|:---------|---------------|--------------------------------------------------------|
| 1 | `node_id`   | `str`      | **YES**  | -             | Node ID to look up                                     |
| 2 | `countries` | `set[str]` | **YES**  | -             | Set of countries to look up offers for                 |
| 3 | `language`  | `str`      | NO       | `"en"`        | Language of responses                                  |
| 5 | `best_only` | `bool`     | NO       | `True`        | Determines whether only best offers should be returned |

Usage of `language` and `best_only` arguments matches the [`search`](#search) command.

Returned value `dict[str, list[Offer]]`, where key is country given as argument and value is a list of [`Offer`](#return-data-structures) tuples.

Example command and its output is in [`examples/offers_for_countries_output.py`](examples/offers_for_countries_output.py).



## Return data structures

Detailed descriptions of all used data structures are available in the [documentation](https://electronic-mango.github.io/simple-justwatch-python-api/simplejustwatchapi.html#module-simplejustwatchapi.query).



## Locale, language, country

Languages and countries are configured via ISO standard.
Countries are following **ISO 3166-1 alpha-2** standard (2-letter codes, uppercase).
Languages are following **ISO 639-1** standard (usually 2-letter codes, lowercase).

Language codes can also be country-specific, e.g. `es-MX` for Mexican Spanish, etc.
The country part **must** be uppercase.

There is a list of supported locales in [JustWatch **REST API** documentation](https://apis.justwatch.com/docs/api/#tips).
Any combination of those languages and countries should work with this API as well.

If you provide unsupported language JustWatch API should default to english.



## Disclaimer

This API is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with JustWatch.
This is an independent and unofficial project.
Use at your own risk.
