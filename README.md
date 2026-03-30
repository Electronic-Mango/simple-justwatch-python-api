# Simple JustWatch Python API

[![PyPi](https://img.shields.io/pypi/v/simple-justwatch-python-api.svg)](https://pypi.python.org/pypi/simple-justwatch-python-api)
[![License](https://img.shields.io/pypi/l/simple-justwatch-python-api.svg)](https://pypi.python.org/pypi/simple-justwatch-python-api)
[![Python versions](https://img.shields.io/pypi/pyversions/simple-justwatch-python-api.svg)](https://pypi.python.org/pypi/simple-justwatch-python-api)
[![CodeQL](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql.yml)
[![Ruff](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/ruff.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/ruff.yml)
[![Pytest](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml)
[![Coverage Status](https://coveralls.io/repos/github/Electronic-Mango/simple-justwatch-python-api/badge.svg?branch=main)](https://coveralls.io/github/Electronic-Mango/simple-justwatch-python-api?branch=main)

A simple unofficial JustWatch Python API which uses [`GraphQL`](https://graphql.org/) to access JustWatch data, built with [`httpx`](https://www.python-httpx.org/) and `Python3.11`.

This project is managed by [uv](https://docs.astral.sh/uv/).



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

For very large searches (high `count` value) I recommend using default `best_only=True` to avoid issues with [request complexity](#request-complexity).

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

This function can be used for all types of media - shows, movies, episodes, seasons (the last two having their dedicated functions described below),
for all types the result is a single [`MediaEntry`](#return-data-structures) object.
Some fields are specific for one of the media types and will be `None` for others - e.g.:
 - `total_episode_count` is only present for seasons
 - `season_number` is present for seasons and episodes
 - `episode_number` is present only for episodes
 - `age_certification` is present only for movies and shows

For episodes specifically most of the fields will be empty (which is why [`episodes`](#episodes) command returns different structure).

Example command and its output is in [`examples/details_output.py`](examples/details_output.py).


### Seasons

Seasons function allows for looking up all seasons of a show via its node ID.
Node/show ID can be taken from output of the [`search`](#search) command.
It's also the same ID as input for [`details`](#details) command.

Each season contains similar data to the [`details`](#details) command, with additional season number and number of episodes.

Usage also matches [`details`](#details) command:
```python
from simplejustwatchapi.justwatch import seasons

results = seasons("nodeID", "US", "en", False)
```

Only the first argument is required - the node ID of element to look up details for.

|   | Argument    | Type   | Required | Default value | Description                                            |
|---|-------------|--------|----------|---------------|--------------------------------------------------------|
| 1 | `show_id`   | `str`  | **YES**  | -             | Node/show ID to look up                                |
| 2 | `country`   | `str`  | NO       | `"US"`        | Country to search for offers                           |
| 3 | `language`  | `str`  | NO       | `"en"`        | Language of responses                                  |
| 5 | `best_only` | `bool` | NO       | `True`        | Determines whether only best offers should be returned |

Returned value is a list of [`MediaEntry`](#return-data-structures) objects, each describing a single season.


### Episodes

Episodes function allows for looking up all episodes of a season via season's node ID.
Node/season ID can be taken from output of the [`seasons`](#seasons) command.

Usage matches [`details`](#details) command:
```python
from simplejustwatchapi.justwatch import seasons

results = seasons("nodeID", "US", "en", False)
```

Only the first argument is required - the node ID of element to look up details for.

|   | Argument    | Type   | Required | Default value | Description                                            |
|---|-------------|--------|----------|---------------|--------------------------------------------------------|
| 1 | `season_id` | `str`  | **YES**  | -             | Node/season ID to look up                              |
| 2 | `country`   | `str`  | NO       | `"US"`        | Country to search for offers                           |
| 3 | `language`  | `str`  | NO       | `"en"`        | Language of responses                                  |
| 5 | `best_only` | `bool` | NO       | `True`        | Determines whether only best offers should be returned |

Returned value is a list of [`Episode`](#return-data-structures) objects, each describing a single episode.
Each contains only a small subset of fields from the [`MediaEntry`](#return-data-structures) object,
JustWatch API doesn't return "full" data.


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

The main structure `MediaEntry` contains fields for all media types - movies, shows, seasons, episodes.
Some fields are specific for one of the media types and will be `None` for others - e.g.:
 - `total_episode_count` is only present for seasons
 - `season_number` is present for seasons and episodes
 - `episode_number` is present only for episodes
 - `age_certification` is present only for movies and shows

For episodes specifically most of the fields will be empty (which is why [`episodes`](#episodes) command returns different structure).

As [`search`](#search) function can return only movies and shows the episode-specific and season-specific fields will always be `None`,
but are included in `MediaEntry` so they will be present in output from [`details`](#details) function.


## Locale, language, country

Languages and countries are configured via ISO standard.
Countries are following **ISO 3166-1 alpha-2** standard (2-letter codes, uppercase).
Languages are following **ISO 639-1** standard (usually 2-letter codes, lowercase).

Language codes can also be country-specific, e.g. `es-MX` for Mexican Spanish, etc.
The country part **must** be uppercase.

There is a list of supported locales in [JustWatch **REST API** documentation](https://apis.justwatch.com/docs/api/#tips).
Any combination of those languages and countries should work with this API as well.

If you provide unsupported language JustWatch API should default to english.



## Request complexity

JustWatch API will respond with error on too high request/response complexity - essentially when returned graph would be too large.
It's the reason for why seasons/episodes data isn't available directly in [`search`](#search), or [`details`](#details) function
(mostly the former).

This issue can still occur for [`search`](#search) with too high `count` value.
In my tests the limit is around 100 (in the worst case with `best_only=False`).
It's a lot, but keep it in mind.

Using `best_only=True` should alleviate the issue somewhat, so for very large requests I recommend using its default `True` value.



## Disclaimer

This API is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with JustWatch.
This is an independent and unofficial project.
Use at your own risk.
