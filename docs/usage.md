---
icon: lucide/hammer
---

# Usage

This library provides multiple functions for accessing JustWatch:

 - `search` - search for entries based on title
 - `popular` - get a list of currently popular titles
 - `details` - get details for a title based on its ID
 - `seasons` - get information about all seasons of a show
 - `episodes` - get information about all episodes of a season
 - `offers_for_countries` - get offers for a title based on its ID for multiple
    countries
 - `providers` - get data about all available providers (like Netflix) in a country

All functions return response from JustWatch API parsed into a [`NamedTuple`]
[typing.NamedTuple], check [Data structures](API Reference/data.md) page for more
details.

All needed functions, data structures, raised exceptions are available through single
module - `simplejustwatchapi`.

Examples of parsed responses are in the GitHub repository in
[`examples/`](https://github.com/Electronic-Mango/simple-justwatch-python-api/tree/\
main/examples).


## Functions

### Common arguments

Most functions have a number of common arguments (in addition to function-specific
ones, like `node_id`, or `title` to search for):

| Name        | Description |
|-------------|-------------|
| `country`   | 2-letter country code for which offers will be returned, e.g., `US`, `GB`, `DE`. |
| `language`  | Language code for responses' language. It can be just basic 2-letter code (e.g., `en`, `de`) or with a IETF BCP 47 suffix for region (e.g., `en-US`, `de-CH`). I don't think this is exactly IETF BCP 47, as the suffix can contain only uppercase letters and numbers. |
| `best_only` | Whether to return only "best" offers for each provider instead of, e.g., separate offer for SD, HD, and 4K. |

Functions returning data for multiple titles
([`search`][simplejustwatchapi.justwatch.search],
[`popular`][simplejustwatchapi.justwatch.popular])
also allow for specifying number of elements, basic pagination, and filtering for
specific providers:

| Name        | Description |
|-------------|-------------|
| `count`     | How many entries should be returned. |
| `offset`    | Basic "pagination", how many first elements should be skipped. Everything is handled on API side, this library isn't doing any filtering. |
| `providers` | Providers (like Netflix, Amazon Prime Video) for which offers should returned. Requires 3-letter "short name". Check [Provider codes](caveats.md#provider-codes) page for an example of how you can get that value.


### Search for a title

Search functions allows for searching entries based on a given title.

```python
from simplejustwatchapi import search

results = search("title", "US", "en", 5, True, 0, {"nfx", "apv"})
```

No arguments are required.

| Argument    | Type   | Default value       | Description                                            |
|-------------|--------|---------------------|--------------------------------------------------------|
| `title`     | `str`  | `""`                | Title to look up                                       |
| `country`   | `str`  | `"US"`              | Country to search for offers                           |
| `language`  | `str`  | `"en"`              | Language of responses                                  |
| `count`     | `int`  | `4`                 | Up to how many entries should be returned              |
| `best_only` | `bool` | `True`              | Determines whether only best offers should be returned |
| `offset`    | `int`  | `0`                 | How many titles should be skipped from the output      |
| `providers` | `list[str] | str | None` | `None` | Determines whether only best offers should be returned |

`title` is just a string to look up. If empty, or not provided, you'll get a selection of popular titles,
similar to [`popular`](#popular) function.

!!! note "Whitespaces in title"
    value of `title` isn't stripped, so passing a string with multiple spaces will look
    them up. For more than 1 space it will (probably) always return an empty list.

`country` must be **ISO 3166-1 alpha-2** 2-letter code , e.g. `US`, `GB`, `FR`.
It should be uppercase, however lowercase codes are automatically converted to uppercase.

`language` is a **ISO 639-1** (usually) 2-letter code, lowercase, e.g. `en`, `fr`.

`count` determines **up to** how many entries should be returned.
If JustWatch GraphQL API returns fewer entries, then this function will also return fewer values.

`best_only` determines whether similar offers, but lower quality should be included in response.
If a platform offers streaming for a given entry in 4K, HD and SD, then `best_only = True` will return only the 4K offer, `best_only = False` will return all three.

`offset` allows for very basic pagination, letting you get more data without running into [operation complexity](caveats.md#operation-complexity).
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

For very large searches (high `count` value) I recommend using default `best_only=True` to avoid issues with [operation complexity](caveats.md#operation-complexity).

Example function call and its output is in [`examples/search_output.py`](examples/search_output.py).



### Popular titles

Look up all currently popular titles.
The usage and output will be similar to [`search`](#search), function without any titles specified.

```python
from simplejustwatchapi import popular

results = popular("US", "en", 5, True, 0, {"nfx", "apv"})
```

No arguments are required.

| Argument    | Type   | Default value       | Description                                            |
|-------------|--------|---------------------|--------------------------------------------------------|
| `country`   | `str`  | `"US"`              | Country to search for titles                           |
| `language`  | `str`  | `"en"`              | Language of responses                                  |
| `count`     | `int`  | `4`                 | Up to how many entries should be returned              |
| `best_only` | `bool` | `True`              | Determines whether only best offers should be returned |
| `offset`    | `int`  | `0`                 | How many titles should be skipped from the output      |
| `providers` | `list[str] | str | None`| `None` | Determines whether only best offers should be returned |

`country` must be **ISO 3166-1 alpha-2** 2-letter code , e.g. `US`, `GB`, `FR`.
It should be uppercase, however lowercase codes are automatically converted to uppercase.

`language` is a **ISO 639-1** (usually) 2-letter code, lowercase, e.g. `en`, `fr`.

`count` determines **up to** how many entries should be returned.
If JustWatch GraphQL API returns fewer entries, then this function will also return fewer values.

`best_only` determines whether similar offers, but lower quality should be included in response.
If a platform offers streaming for a given entry in 4K, HD and SD, then `best_only = True` will return only the 4K offer, `best_only = False` will return all three.

`offset` allows for very basic pagination letting you get more data without running into [operation complexity](caveats.md#operation-complexity).
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

For very large searches (high `count` value) I recommend using default `best_only=True` to avoid issues with [operation complexity](caveats.md#operation-complexity).

Example function call and its output is in [`examples/popular_output.py`](examples/popular_output.py).


### Details for a title based on its ID

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

| Argument    | Type   | Default value | Description                                            |
|-------------|--------|---------------|--------------------------------------------------------|
| `node_id`   | `str`  | -             | **Required** node ID to look up                        |
| `country`   | `str`  | `"US"`        | Country to search for offers                           |
| `language`  | `str`  | `"en"`        | Language of responses                                  |
| `best_only` | `bool` | `True`        | Determines whether only best offers should be returned |

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


### Details for all seasons of a TV show

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

| Argument    | Type   | Default value | Description                                            |
|-------------|--------|---------------|--------------------------------------------------------|
| `show_id`   | `str`  | -             | **Required** node/show ID to look up                   |
| `country`   | `str`  | `"US"`        | Country to search for offers                           |
| `language`  | `str`  | `"en"`        | Language of responses                                  |
| `best_only` | `bool` | `True`        | Determines whether only best offers should be returned |

Returned value is a list of [`MediaEntry`](#return-data-structures) objects, each describing a single season.


### Details for all episodes of a TV show

Episodes function allows for looking up all episodes of a season via season's node ID.
Node/season ID can be taken from output of the [`seasons`](#seasons) function.

Usage matches [`details`](#details) function:
```python
from simplejustwatchapi import seasons

results = seasons("nodeID", "US", "en", False)
```

Only the first argument is required - the node ID of element to look up details for.

| Argument    | Type   | Default value | Description                                            |
|-------------|--------|---------------|--------------------------------------------------------|
| `season_id` | `str`  | -             | **Required** node/season ID to look up                 |
| `country`   | `str`  | `"US"`        | Country to search for offers                           |
| `language`  | `str`  | `"en"`        | Language of responses                                  |
| `best_only` | `bool` | `True`        | Determines whether only best offers should be returned |

Returned value is a list of [`Episode`](#return-data-structures) objects, each describing a single episode.
Each contains only a small subset of fields from the [`MediaEntry`](#return-data-structures) object,
JustWatch API doesn't return "full" data.


### Get offers for multiple countries for a single title

This function allows looking up offers for entry by given node ID.
It allows specifying a set of countries, instead of a single one.
This way you can simultaneously look up offers for multiple countries.

```python
from simplejustwatchapi import offers_for_countries

results = offers_for_countries("nodeID", {"US", "UK", "CA"}, "en", True)
```

First two arguments are required - node ID, and set of countries.

| Argument    | Type       | Default value | Description                                            |
|-------------|------------|---------------|--------------------------------------------------------|
| `node_id`   | `str`      | -             | **Required** node ID to look up                        |
| `countries` | `set[str]` | -             | **Required** set of countries to look up offers for    |
| `language`  | `str`      | `"en"`        | Language of responses                                  |
| `best_only` | `bool`     | `True`        | Determines whether only best offers should be returned |

Usage of `language` and `best_only` arguments matches the [`search`](#search) function.

Returned value `dict[str, list[Offer]]`, where key is country given as argument and value is a list of [`Offer`](#return-data-structures) tuples.

Example function call and its output is in [`examples/offers_for_countries_output.py`](examples/offers_for_countries_output.py).


### Get all available providers for a country

Get all available service providers ("Netflix", "Amazon Prime Video, etc.) for a given country.

```python
from simplejustwatchapi import providers

results = providers("US")
```

| Argument    | Type   | Default value | Description                     |
|-------------|--------|---------------|---------------------------------|
| `country`   | `str`  | `"US"`        | Country to search for providers |

`country` must be **ISO 3166-1 alpha-2** 2-letter code , e.g. `US`, `GB`, `FR`.
It should be uppercase, however lowercase codes are automatically converted to uppercase.

Returned value is a list of `OfferPackage` tuples.
Initially they were meant to be used for `Offer` in `MediaEntry`/`Episode`, however the data structure
matches output here, so it's reused.

You can use this function to get values for providers for [`search`](#search) and [`popular`](#popular) functions,
the `short_name` field in returned `OfferPackage` tuples is the exact 3-letter code needed there.

Example function call and its output is in [`examples/providers_output.py`](examples/providers_output.py).



## Error handling

Each function can raise two exceptions:

| Exception                                                                | Cause |
|--------------------------------------------------------------------------|-------|
| [`JustWatchHttpError`][simplejustwatchapi.exceptions.JustWatchHttpError] | JustWatch API responded with non-`2xx` code. |
| [`JustWatchApiError`][simplejustwatchapi.exceptions.JustWatchApiError]   | JSON response from JustWatch API contains errors,<br>even though the API responded with a `2xx` status code. |

You can check [Exceptions](API Reference/exceptions.md) page for more details.

### HTTP errors

Non-`2xx` response status codes can happen when trying to use incorrect type for
parameters, e.g., trying to use a non-numeric string for `count`:

```python
from simplejustwatchapi import search, JustWatchHttpError

try:
    results = search("The Matrix", count="five")
except JustWatchHttpError as e:
    print(e.code, e.message)
    # In this case "e.message" is a JSON, but handled as a regular string.
```

!!! note "Numeric strings instead of `int`"
    Since requests are send as a JSON you can use strings for `int` arguments, as long
    as they are numeric strings, like `5`, instead of `five`:

    ```python
    from simplejustwatchapi import search

    results = search("The Matrix", count="5")
    # No exception is raised.
    ```


### API errors

API errors can occur for invalid country code:
```python
from simplejustwatchapi import search, JustWatchApiError

try:
    # Country code matches 2-letter pattern, but isn't a valid code for any country.
    results = search("The Matrix", country="xx")
except JustWatchApiError as e:
    # Print all error messages.
    error_messages = [error.get("message") for error in e.errors]
    print(",".join(error_messages))
```

It can occur for language codes not matching expected pattern:
```python
from simplejustwatchapi import search, JustWatchApiError

try:
    # Language code "xx" also isn't valid for any languages, but since it matches the
    # pattern it would default to english.
    results = search("The Matrix", language="xxx")
except JustWatchApiError as e:
    # Print only error codes.
    # Codes are collected to a set, as the API will return an error for each place,
    # where language code is used, in all offers, descriptions, etc.
    error_codes = {error["extensions"]["code"] for error in e.errors}
    print(",".join(error_codes))
```

Using title, instead of ID in [`details`][simplejustwatchapi.justwatch.details]
function:

```python
from simplejustwatchapi import details, JustWatchError

try:
    # "details" expects an ID, not a title.
    results = details("The Matrix")
except JustWatchError as e:
    # JustWatchError will catch both API and HTTP exceptions.
    print(e.errors)
```

Too high operation complexity due to too large `count`:

```python
from simplejustwatchapi import search, JustWatchApiError

try:
    results = search("The Matrix", count=500)
except JustWatchApiError as e:
    error_messages = [error.get("message") for error in e.errors]
    print(",".join(error_messages))
```

And, probably, many other, similar, cases as well.


## Advanced examples
