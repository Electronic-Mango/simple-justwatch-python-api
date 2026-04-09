---
icon: lucide/hammer
---

# Usage

This library provides multiple functions for accessing JustWatch:

 - [`search`](#search-for-a-title) - search for entries based on title
 - [`popular`](#popular-titles) - get a list of currently popular titles
 - [`details`](#details-for-a-title-based-on-its-id) - get details for a title based on
    its ID
 - [`seasons`](#details-for-all-seasons-of-a-tv-show) - get information about all
    seasons of a show
 - [`episodes`](#details-for-all-episodes-of-a-tv-show) - get information about all
    episodes of a season
 - [`offers_for_countries`](#get-offers-for-multiple-countries-for-a-single-title) - get
    offers for a title for multiple countries simultaneously 
 - [`providers`](#get-all-available-providers-for-a-country) - get data about all
    available providers (like Netflix) in a country

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
ones, like `title` to search for):

| Name        | Description |
|-------------|-------------|
| `country`   | 2-letter country code for which offers will be returned, e.g., `US`, `GB`, `DE`. |
| `language`  | Language code for responses' language. It can be just basic 2-letter code (e.g., `en`, `de`) or with a IETF BCP 47 suffix (e.g., `en-US`, `de-CH1901`). I don't think this is exactly IETF BCP 47, as the suffix can contain only uppercase letters and numbers. |
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

[`search`][simplejustwatchapi.justwatch.search] function allows for searching entries
based on a given title.

```python
from simplejustwatchapi import search

results = search("The Matrix", "US", "en", 5, True, 0, ["nfx", "apv"])
for entry in results:
    print(entry.title, entry.offers)
```

All arguments are optional.

First argument is just a string to look up. If empty, or not provided, you'll get a
selection of popular titles, similar to [`popular`](#popular) function.

!!! note "Whitespaces in title"
    value of `title` isn't stripped, so passing a string with multiple spaces will look
    them up. For more than 1 space it will (probably) always return an empty list.

For very large searches (high `count` value) I recommend using default `best_only=True`
to avoid issues with [operation complexity](caveats.md#operation-complexity).
Alternatively you can `offset` for
[basic pagination](caveats.md#getting-more-results-and-pagination).

Example function call and its output is in
[`examples/search_output.py`](https://github.com/Electronic-Mango/simple-justwatch-python-api/blob/main/examples/search_output.py).



### Popular titles

[`popular`][simplejustwatchapi.justwatch.popular] function allows for getting a list of
currently popular titles.

```python
from simplejustwatchapi import popular

results = popular("US", "en", 5, True, 0, ["nfx", "apv"])
for entry in results:
    print(entry.title, entry.offers)
```

All arguments are optional.

The usage and output will be similar to [`search`](#search-for-a-title), function
without any titles specified.

No arguments are required.

For very large searches (high `count` value) I recommend using default `best_only=True`
to avoid issues with [operation complexity](caveats.md#operation-complexity).
Alternatively you can `offset` for
[basic pagination](caveats.md#getting-more-results-and-pagination).

Example function call and its output is in
[`examples/popular_output.py`](https://github.com/Electronic-Mango/simple-justwatch-python-api/blob/main/examples/popular_output.py).


### Details for a title based on its ID

[`details`][simplejustwatchapi.justwatch.details] function allows for looking up details
for a single entry via its node ID.

```python
from simplejustwatchapi import details

result = details("tm19698", "US", "en", False)
print(result.title, result.short_description)
```

Node ID can be taken from output of the [`search`](#search-for-a-title) function.

!!! note "Usefulness versus [`search`](#search-for-a-title)"
    This function is only useful if you have node ID already stored. There's no reason
    to first use the [`search`](#search-for-a-title), then use node ID from one of
    entries for `details`, you won't get any additional information.

Only the first argument is required - the node ID of element to look up details for.

This function can be used for all types of media - shows, movies, episodes, seasons
(the last two having their dedicated functions described below), for all types the
result is a single [`MediaEntry`][simplejustwatchapi.tuples.MediaEntry]. Some fields
are specific for one of the media types and will be `None` for others - for example:
 - `total_episode_count` is only present for seasons
 - `season_number` is present for seasons and episodes
 - `episode_number` is present only for episodes
 - `age_certification` is present only for movies and shows

For episodes specifically most of the fields will be empty (which is why
[`episodes`](#details-for-all-episodes-of-a-tv-show) function returns different
structure).

Example function call and its output is in
[`examples/details_output.py`](https://github.com/Electronic-Mango/simple-justwatch-python-api/blob/main/examples/details_output.py).


### Details for all seasons of a TV show

[`seasons`][simplejustwatchapi.justwatch.seasons] function allows for looking up details
for all seasons of a TV show based on its node ID.

```python
from simplejustwatchapi import seasons

results = seasons("tss20091", "US", "en", True)
for season in results:
    print(season.season_number, season.total_episode_count)
```

Only the first argument is required - the node ID of a TV show to look up season
details for.

Example function call and its output is in
[`examples/seasons_output.py`](https://github.com/Electronic-Mango/simple-justwatch-python-api/blob/main/examples/seasons_output.py).


### Details for all episodes of a TV show

[`episodes`][simplejustwatchapi.justwatch.episodes] function allows for looking up
details for all episodes of a single TV show season based on its node ID.

```python
from simplejustwatchapi import episodes

results = episodes("tse334769", "US", "en", False)
for episode in results:
    print(episode.episode_id, episode.episode_number, episode.offers)
```

Only the first argument is required - the node ID of a season to look up episode details
for.

Returned value is a list of [`Episode`][simplejustwatchapi.tuples.Episode], which
contains only a small subset of fields from the [`MediaEntry`]
[simplejustwatchapi.tuples.MediaEntry]. JustWatch API doesn't return "full" data for
individual episodes.

Example function call and its output is in
[`examples/episodes_output.py`](https://github.com/Electronic-Mango/simple-justwatch-python-api/blob/main/examples/episodes_output.py).


### Get offers for multiple countries for a single title

[`offers_for_countries`][simplejustwatchapi.justwatch.offers_for_countries] function
allows for looking up offers for a single entry, but for multiple countries at once.
Only offers are returned, not additional data.

```python
from simplejustwatchapi import offers_for_countries

results = offers_for_countries("tm10", {"US", "UK", "CA"}, "en", True)
for country, offers in results.items():
    print(f"Offers for {country}:")
    for offer in offers:
        print(f"  - {offer.package.name}: {offer.monetization_type}")
```

First two arguments are required - ID, and a set of country codes.

Example function call and its output is in
[`examples/offers_for_countries_output.py`](https://github.com/Electronic-Mango/simple-justwatch-python-api/blob/main/examples/offers_for_countries_output.py).


### Get all available providers for a country

[`providers`][simplejustwatchapi.justwatch.providers] function allows for looking up
all available service providers (such as "Netflix", "Amazon Prime Video", etc.) for a
given country.

```python
from simplejustwatchapi import providers

results = providers("US")
netflix_apple_only = [
    provider
    for provider in all_providers
    if provider.name in ("Netflix", "Apple TV")
]
```

Returned value is a list of [`OfferPackage`][simplejustwatchapi.tuples.OfferPackage].
Initially they were meant to be used for [`Offer`][simplejustwatchapi.tuples.Offer] in
[`MediaEntry`][simplejustwatchapi.tuples.MediaEntry]/[`Episode`]
[simplejustwatchapi.tuples.Episode], however the data structure matches output here, so
it's reused.

You can use this function to get values for providers for
[`search`](#search-for-a-title) and [`popular`](#popular-titles) functions, the
`short_name` field in [`OfferPackage`][simplejustwatchapi.tuples.OfferPackage] is the
exact 3-letter code needed there.

Example function call and its output is in
[`examples/providers_output.py`](https://github.com/Electronic-Mango/simple-justwatch-python-api/blob/main/examples/providers_output.py).



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

And so on.


## Multi-function examples

Small collection of examples of how you can combine multiple functions together.

### Get popular titles for only specific providers

You can combine [`providers`](#get-all-available-providers-for-a-country) and
[`popular`](#popular-titles) functions:
```python
from simplejustwatchapi import popular, providers

# Get all providers in the US.
all_providers = providers("US")

# Filter only required providers by name.
netflix_apple_only = [
    provider.short_name  # We only need the codes for filtering.
    for provider in all_providers
    if provider.name in ("Netflix", "Apple TV")  # Get providers we need.
]

# Use found codes for filtering.
filtered_popular = popular("US", providers=netflix_apple_only)
```


### Get offers for each episode of a TV show based on title

You can combine [`search`](#search-for-a-title),
[`seasons`](#details-for-all-seasons-of-a-tv-show) and
[`episodes`](#details-for-all-episodes-of-a-tv-show) functions:
```python
from simplejustwatchapi import episodes, search, seasons

title = "True Detective"

# Search for a title.
search_results = search(title)

# Look for a first match with the expected title.
first_match = next(
    result
    for result in search_results
    if result.title == title and result.object_type == "SHOW"
)

# Get all seasons.
all_seasons = seasons(first_match.entry_id)

# Create a dict with episode offers.
id_to_episodes_offers = {
    season.season_number: {
        episode.episode_number: episode.offers
        for episode in episodes(season.entry_id)
    }
    for season in all_seasons
}
```


### Get offers for multiple countries for all seasons of a TV show

You can combine [`search`](#search-for-a-title),
[`seasons`](#details-for-all-seasons-of-a-tv-show) and
[`offers_for_countries`](#get-offers-for-multiple-countries-for-a-single-title)
functions:
```python
from simplejustwatchapi import offers_for_countries, search, seasons

title = "Andor"

# Search for a title.
search_results = search(title)

# Look for a first match with the expected title.
first_match = next(
    result
    for result in search_results
    if result.title == title and result.object_type == "SHOW"
)

# Get all seasons.
all_seasons = seasons(first_match.entry_id)

# Get offers for each season for each country.
countries = {"US", "DE"}
season_offers = [
    offers_for_countries(season.entry_id, countries)
    for season in all_seasons
]

# Convert to a dict of country codes to list of offers.
season_offers_per_country = {
    country: [
        season[country]
        for season in season_offers
    ]
    for country in countries
}
```
