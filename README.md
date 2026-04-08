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

- [Installation](#installation)
- [Usage](#usage)
  - [Search](#search)
  - [Popular](#popular)
  - [Details](#details)
  - [Seasons](#seasons)
  - [Episodes](#episodes)
  - [Offers for countries](#offers-for-countries)
  - [Providers](#providers)
- [Data structures](#data-structures)
- [Locale, language, country](#locale-language-country)
- [Operation complexity](#operation-complexity)
- [Maximum number of entries](#maximum-number-of-entries)
- [Provider codes](#provider-codes)
  - [`providers` function](#providers-function)
  - [Query parameters from JustWatch](#query-parameters-from-justwatch)
  - [Stored output from other functions with offers](#stored-output-from-other-functions-with-offers)
- [TODO](#todo)
- [Disclaimer](#disclaimer)


## Installation

Project is available in [PyPi](https://pypi.org/project/simple-justwatch-python-api/):
```bash
pip install simple-justwatch-python-api
```



## Usage

This Python library has multiple functions:

 - [`search`](#search) - search for entries based on title
 - [`popular`](#popular) - get a list of currently popular titles
 - [`details`](#details) - get details for entry based on its node ID
 - [`seasons`](#seasons) - get information about all seasons of a show
 - [`episodes`](#episodes) - get information about all episodes of a season
 - [`offers_for_countries`](#offers-for-countries) - get offers for entry based on its node ID,
   can look for offers in multiple countries
 - [`providers`](#providers) - get data about available providers (e.g., Netflix)

Detailed documentation is available in https://electronic-mango.github.io/simple-justwatch-python-api/.

Example outputs from all functions are in [`examples/`](examples/) directory.


### Search
Search functions allows for searching entries based on a given title.

```python
from simplejustwatchapi import search

results = search("title", "US", "en", 5, True, 0, {"nfx", "apv"})
```

No arguments are required.

|   | Argument    | Type   | Required | Default value       | Description                                            |
|---|-------------|--------|----------|---------------------|--------------------------------------------------------|
| 1 | `title`     | `str`  | NO       | -                   | Title to look up                                       |
| 2 | `country`   | `str`  | NO       | `"US"`              | Country to search for offers                           |
| 3 | `language`  | `str`  | NO       | `"en"`              | Language of responses                                  |
| 4 | `count`     | `int`  | NO       | `4`                 | Up to how many entries should be returned              |
| 5 | `best_only` | `bool` | NO       | `True`              | Determines whether only best offers should be returned |
| 6 | `offset`    | `int`  | NO       | `0`                 | How many titles should be skipped from the output      |
| 7 | `providers` | `list[str] \| str \| None`| NO | `None` | Determines whether only best offers should be returned |

`title` is just a string to look up. If empty, or not provided, you'll get a selection of popular titles,
similar to [`popular`](#popular) function.

> **Note**: value of `title` isn't stripped, so passing a string
with multiple spaces will look them up. For more than 1 space it will (probably) always return an empty list.

`country` must be **ISO 3166-1 alpha-2** 2-letter code , e.g. `US`, `GB`, `FR`.
It should be uppercase, however lowercase codes are automatically converted to uppercase.

`language` is a **ISO 639-1** (usually) 2-letter code, lowercase, e.g. `en`, `fr`.

`count` determines **up to** how many entries should be returned.
If JustWatch GraphQL API returns fewer entries, then this function will also return fewer values.

`best_only` determines whether similar offers, but lower quality should be included in response.
If a platform offers streaming for a given entry in 4K, HD and SD, then `best_only = True` will return only the 4K offer, `best_only = False` will return all three.

`offset` allows for very basic pagination, letting you get more data without running into [operation complexity](#operation-complexity).
It simply skips `offset` number of first entries (on the API side, nothing is done inside the library).
Since there is no session there's no guarantee of results "stability" - if JustWatch decides to
shuffle returned values (I'm not sure what would be the reason, but in theory it's possible)
you might get repeats, or missing entries. It's also not possible to get **all** the data,
only up to 1999, check [Maximum number of entries](#maximum-number-of-entries) for details.

`providers` is a selection of (usually) **3-letter** identifiers for a service provider ("Netflix", "Amazon Prime Video", etc.).
It can be either a list, or (for single providers) a string.
`None` (used as default) turns off any filtering based on providers.
You can get the possible values through [`providers`](#providers) function and `short_name` field from returned `OfferPackage` NamedTuples,
or check [Provider codes](#provider-codes) for more details.

Returned value is a list of [`MediaEntry`](#return-data-structures) objects.

For very large searches (high `count` value) I recommend using default `best_only=True` to avoid issues with [operation complexity](#operation-complexity).

Example function call and its output is in [`examples/search_output.py`](examples/search_output.py).


### Popular
Look up all currently popular titles.
The usage and output will be similar to [`search`](#search), function without any titles specified.

```python
from simplejustwatchapi import popular

results = popular("US", "en", 5, True, 0, {"nfx", "apv"})
```

No arguments are required.

|   | Argument    | Type   | Required | Default value       | Description                                            |
|---|-------------|--------|----------|---------------------|--------------------------------------------------------|
| 1 | `country`   | `str`  | NO       | `"US"`              | Country to search for titles                           |
| 2 | `language`  | `str`  | NO       | `"en"`              | Language of responses                                  |
| 3 | `count`     | `int`  | NO       | `4`                 | Up to how many entries should be returned              |
| 4 | `best_only` | `bool` | NO       | `True`              | Determines whether only best offers should be returned |
| 5 | `offset`    | `int`  | NO       | `0`                 | How many titles should be skipped from the output      |
| 6 | `providers` | `list[str] \| str \| None`| NO | `None` | Determines whether only best offers should be returned |

`country` must be **ISO 3166-1 alpha-2** 2-letter code , e.g. `US`, `GB`, `FR`.
It should be uppercase, however lowercase codes are automatically converted to uppercase.

`language` is a **ISO 639-1** (usually) 2-letter code, lowercase, e.g. `en`, `fr`.

`count` determines **up to** how many entries should be returned.
If JustWatch GraphQL API returns fewer entries, then this function will also return fewer values.

`best_only` determines whether similar offers, but lower quality should be included in response.
If a platform offers streaming for a given entry in 4K, HD and SD, then `best_only = True` will return only the 4K offer, `best_only = False` will return all three.

`offset` allows for very basic pagination letting you get more data without running into [operation complexity](#operation-complexity).
It simply skips first entries (on the API side, nothing is done inside the library).
Since there is no session there's no guarantee of results "stability" - if JustWatch decides to
shuffle returned values (I'm not sure what would be the reason, but in theory it's possible)
you might get repeats, or missing entries. It's also not possible to get **all** the data,
only up to 2000, check [Maximum number of entries](#maximum-number-of-entries) for details.

`providers` is a selection of (usually) **3-letter** identifiers for a service provider ("Netflix", "Amazon Prime Video", etc.).
It can be either a list, or (for single providers) a string.
`None` (used as default) turns off any filtering based on providers.
You can get the possible values through [`providers`](#providers) function and `short_name` field from returned `OfferPackage` NamedTuples,
or check [Provider codes](#provider-codes) for more details.

Returned value is a list of [`MediaEntry`](#return-data-structures) objects.

For very large searches (high `count` value) I recommend using default `best_only=True` to avoid issues with [operation complexity](#operation-complexity).

Example function call and its output is in [`examples/popular_output.py`](examples/popular_output.py).

### Details

Details function allows for looking up details for a single entry via its node ID.
Node ID can be taken from output of the [`search`](#search) function.

Output from this function contains the same data as a single entry from the [`search`](#search) function.

> **In general using this function is only useful if you have node ID already stored.**
There's no reason to first use the [`search`](#search) function, then use node ID from one of entries for `details`, you won't get any additional information.
If you want to get seasons/episodes you can use the ID from [`search`](#search) function to call [`seasons`](#seasons), and then [`episodes`](#episodes). Calling `details` on an individual season/episode won't give you more information than outputs from the dedicated functions.

Usage is similar to [`search`](#search) function, just without `count` argument:
```python
from simplejustwatchapi import details

results = details("nodeID", "US", "en", False)
```

Only the first argument is required - the node ID of element to look up details for.

|   | Argument    | Type   | Required | Default value | Description                                            |
|---|-------------|--------|----------|---------------|--------------------------------------------------------|
| 1 | `node_id`   | `str`  | **YES**  | -             | Node ID to look up                                     |
| 2 | `country`   | `str`  | NO       | `"US"`        | Country to search for offers                           |
| 3 | `language`  | `str`  | NO       | `"en"`        | Language of responses                                  |
| 5 | `best_only` | `bool` | NO       | `True`        | Determines whether only best offers should be returned |

General usage of these arguments matches the [`search`](#search) function.

Returned value is a single [`MediaEntry`](#return-data-structures) object.

This function can be used for all types of media - shows, movies, episodes, seasons (the last two having their dedicated functions described below),
for all types the result is a single [`MediaEntry`](#return-data-structures) object.
Some fields are specific for one of the media types and will be `None` for others - e.g.:
 - `total_episode_count` is only present for seasons
 - `season_number` is present for seasons and episodes
 - `episode_number` is present only for episodes
 - `age_certification` is present only for movies and shows

For episodes specifically most of the fields will be empty (which is why [`episodes`](#episodes) function returns different structure).

Example function call and its output is in [`examples/details_output.py`](examples/details_output.py).


### Seasons

Seasons function allows for looking up all seasons of a show via its node ID.
Node/show ID can be taken from output of the [`search`](#search) function.
It's also the same ID as input for [`details`](#details) function.

Each season contains similar data to the [`details`](#details) function, with additional season number and number of episodes.

Usage also matches [`details`](#details) function:
```python
from simplejustwatchapi import seasons

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
Node/season ID can be taken from output of the [`seasons`](#seasons) function.

Usage matches [`details`](#details) function:
```python
from simplejustwatchapi import seasons

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
from simplejustwatchapi import offers_for_countries

results = offers_for_countries("nodeID", {"US", "UK", "CA"}, "en", True)
```

First two arguments are required - node ID, and set of countries.

|   | Argument    | Type       | Required | Default value | Description                                            |
|---|-------------|------------|:---------|---------------|--------------------------------------------------------|
| 1 | `node_id`   | `str`      | **YES**  | -             | Node ID to look up                                     |
| 2 | `countries` | `set[str]` | **YES**  | -             | Set of countries to look up offers for                 |
| 3 | `language`  | `str`      | NO       | `"en"`        | Language of responses                                  |
| 5 | `best_only` | `bool`     | NO       | `True`        | Determines whether only best offers should be returned |

Usage of `language` and `best_only` arguments matches the [`search`](#search) function.

Returned value `dict[str, list[Offer]]`, where key is country given as argument and value is a list of [`Offer`](#return-data-structures) tuples.

Example function call and its output is in [`examples/offers_for_countries_output.py`](examples/offers_for_countries_output.py).


### Providers

Get all available service providers ("Netflix", "Amazon Prime Video, etc.) for a given country.

```python
from simplejustwatchapi import providers

results = providers("US")
```

|   | Argument    | Type   | Required | Default value | Description                     |
|---|-------------|--------|----------|---------------|---------------------------------|
| 1 | `country`   | `str`  | NO       | `"US"`        | Country to search for providers |

`country` must be **ISO 3166-1 alpha-2** 2-letter code , e.g. `US`, `GB`, `FR`.
It should be uppercase, however lowercase codes are automatically converted to uppercase.

Returned value is a list of `OfferPackage` tuples.
Initially they were meant to be used for `Offer` in `MediaEntry`/`Episode`, however the data structure
matches output here, so it's reused.

You can use this function to get values for providers for [`search`](#search) and [`popular`](#popular) functions,
the `short_name` field in returned `OfferPackage` tuples is the exact 3-letter code needed there.

Example function call and its output is in [`examples/providers_output.py`](examples/providers_output.py).



## Data structures

Detailed descriptions of all used data structures are available in the [documentation](https://electronic-mango.github.io/simple-justwatch-python-api).

The main structure `MediaEntry` contains fields for all media types - movies, shows, seasons, episodes.
Some fields are specific for one of the media types and will be `None` for others - e.g.:
 - `total_episode_count` is only present for seasons
 - `season_number` is present for seasons and episodes
 - `episode_number` is present only for episodes
 - `age_certification` is present only for movies and shows

For episodes specifically most of the fields will be empty (which is why [`episodes`](#episodes) function returns different structure).

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



## Operation complexity

JustWatch API will respond with error on too high operation complexity - essentially when returned graph would be too large.
It's the reason for why seasons/episodes data isn't available directly in [`search`](#search), or [`details`](#details) function
(mostly the former).

This issue can still occur for [`search`](#search) with too high `count` value.
In my tests the limit is around 100 (in the worst case with `best_only=False`).
It's a lot, but keep it in mind.

Using `best_only=True` should alleviate the issue somewhat, so for very large requests I recommend using its default `True` value.



## Maximum number of entries

The JustWatch API itself won't allow for getting more than 1999 entries, through `count` and `offset`, regardless of operation complexity.
If you try to get the 2000th entry the API (and functions in this libary) will return an empty list.

**If you try to access over the 1999th entry you won't get *up to* 1999 entries, you'll get an empty list.**

For example, this will get you entries 1990 - 1999 - a 9 element list of `MediaEntry`, as expected:

```python
from simplejustwatchapi import search

results = search("title", count=9, offset=1990)
# len(results) == 9, as expected
```

But trying to get 1990 - 2000 will result in an empty list:

```python
from simplejustwatchapi import search

results = search("title", count=10, offset=1990)
# len(results) == 0, API responded with empty list
```

Overshooting will also result in an empty list:

```python
from simplejustwatchapi import search

results = search("title", count=100, offset=1950)
# len(results) == 0, API responded with empty list
```

Interestingly, you'll still hit [too high operation complexity](#operation-complexity)
for too high values of `count`, even though you'd get an empty list anyway:

```python
from simplejustwatchapi import search

results = search("title", count=200, offset=1950)
# Errors out due to complexity
```



## Provider codes

One note to keep in mind - the codes can be different for different countries.


### [`providers`](#providers) function

The easiest way of getting all provider codes for filtering in [`search`](#search) and [`popular`](#popular) functions
is through [`providers`](#providers) function, for example:

```python
from simplejustwatchapi import popular, providers

codes = [
    package.short_name
    for package
    in providers("GB")  # Look up all providers in the UK.
    if package.name in ("Netflix", "Amazon Prime Video")  # Only get codes for specific providers
]

# codes == ["nfx", "amp"]

# Get popular titles only for selected providers:
popular_netflix_amazon = popular(providers=codes)
```


### Query parameters from JustWatch

You can also get them by going to [JustWatch main page](https://www.justwatch.com/)
and selecting **at least 2** of available services.
**You need 2**, for 1 you'll get its full name.
Only for multiple you'll get the needed codes as `?providers=<code1>+<code2>+...` query parameter,
for example on US version the URL when selecting "Netflix" and "Amazon Prime Video" is:

```url
https://www.justwatch.com/us?providers=amp,nfx
```

So the codes for them are `amp` and `nfx` for the US.


### Stored output from other functions with offers

The codes are also returned when looking up offers (through pretty much any function aside from `providers`) through `OfferPackage` and its `short_name` field.
For example, to get a `dict` "**full name**": "**code**" you can:

```python
from simplejustwatchapi import search

results = search("title", "US", "en", 5, True)
name_to_code_dict = {
    offer.package.name: offer.package.short_name  # Get name and short_name/code from packages
    for entry in results  # Iterate all entries
    for offer in entry.offers  # Iterate all offers per entry
}
```



## TODO

 - [x] Add another custom exception for invalid language code.
JustWatch reports expected regex: `^[a-z]{2}(-[0-9A-Z]+)?$`.
It seems to be a combination of ISO 639-1 and BCP 47 subtags.
 - [x] Improve checking for country code validity - JustWatch rports expected regex: `^[A-Z]{2}$` - better than just length.
 - [ ] Should exceptions be raised in `justwatch.py`, or in `query.py`?



## Disclaimer

This library is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with JustWatch.
This is an independent and unofficial project.
Use at your own risk.
