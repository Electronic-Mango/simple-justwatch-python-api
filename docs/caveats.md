---
icon: lucide/notebook-pen
---

# Caveats

## Data structures

### Type-specific fields in [`MediaEntry`][simplejustwatchapi.tuples.MediaEntry]

The main structure [`MediaEntry`][simplejustwatchapi.tuples.MediaEntry] contains fields
for all media types - movies, shows, seasons, episodes. Some fields are specific for one
of the media types and will be `None` for others - e.g.:

 - `total_episode_count` is only present for seasons
 - `season_number` is present for seasons and episodes
 - `episode_number` is present only for episodes
 - `age_certification` is present only for movies and shows

For episodes specifically most of the fields will be empty - which is why [`episodes`]
[simplejustwatchapi.justwatch.episodes] function returns different structure [`Episode`]
[simplejustwatchapi.tuples.Episode].

As [`search`][simplejustwatchapi.justwatch.search] function can return only movies and
shows, the episode-specific and season-specific fields will always be `None`.
They are included in [`MediaEntry`][simplejustwatchapi.tuples.MediaEntry] so they will
be present in output from [`details`][simplejustwatchapi.justwatch.details] function
and to reuse the structure in [`seasons`][simplejustwatchapi.justwatch.seasons].


### Optional fields

Some fields in returned data is marked as optional (through `| None`). Since there is no
documentation for the JustWatch GraphQL API I tried to mark as optional fields which I
found to **actually** be optional, rather than mark everything.

However, there is no guarantee what the API will return, so if you need maximum safety
you might need to treat **all** fields as effectively optional (as in - they can be
`None`).



## Locale, language, country

Languages and countries are configured via their respecive codes. While the JustWatch
API does not give specific standards, it will respond with an error with expected code
regex for invalid ones. You can infer the standard from the regex, however it might not
be strict.

There is **a** list of supported locales in
[JustWatch **REST API** documentation](https://apis.justwatch.com/docs/api/#tips).
Any combination of those languages and countries should work with this API as well, but
it doesn't seem to be comprehensive.


### Country

Required pattern is two uppercase letters (e.g., `US`, `DE`, `GB`):
```regex
^[A-Z]{2}$
```

It looks like **ISO 3166-1 alpha-2** standard.

!!! tip "Country code letter case"
    API expects only uppercase letters, however this library will automatically convert
    country codes to uppercase.

If country code doesn't match the regex, or isn't a valid code the API will respond
with an internal error and [`JustWatchApiError`]
[simplejustwatchapi.exceptions.JustWatchApiError] will be raised.


### Language

Required pattern is 2 lowercase letters with optional
alphanumeric suffix after `-` (e.g., `en`, `en-US`, `fr`, `de`, `de-CH`, `de-CH1901`).
The sufix must be uppercase:
```
^[a-z]{2}(-[0-9A-Z]+)?$
```

It looks similar to **IETF BCP 47** standard, without `-` characters in the suffix.

!!! warning "Language code letter case"
    The provided language isn't modified at all by this library, so it must match the
    regex exactly, including letter case.

If language code doesn't match the expected regex the API will respond with an internal
error and [`JustWatchApiError`][simplejustwatchapi.exceptions.JustWatchApiError] will be
raised.

If the code **does** match the regex, but isn't a valid code, then the API defaults to
English and no exception is raised.

!!! note "Discrepancy between invalid country and language codes"
    API handles codes matching expected pattern, but still not valid differently between
    country and language - for country API will return and error, thus exception will
    be raised; while for language it will default to English.



## Operation complexity

JustWatch API will respond with error on too high operation complexity -
essentially when returned graph would be too large. It's the reason for why
seasons/episodes data isn't available directly in
[`search`][simplejustwatchapi.justwatch.search],
[`popular`][simplejustwatchapi.justwatch.popular], or
[`details`][simplejustwatchapi.justwatch.details] functions (mostly the first one).

This issue can still occur for [`search`][simplejustwatchapi.justwatch.search] and
[`popular`][simplejustwatchapi.justwatch.popular] with too high `count` value.
In my tests the limit is around 100 (in the worst case with `best_only = False`).
It's a lot, but keep it in mind.

Using `best_only=True` should alleviate the issue somewhat, so for very large requests I
recommend using its default `True` value.

If you need even more entries you can retrieve data in
[chunks using `offset` parameter](#getting-more-results-and-pagination).



## Maximum number of entries

The JustWatch API itself won't allow for getting more than 1999 entries, through `count`
and `offset`, regardless of operation complexity. If you try to get the 2000th entry,
the API (and functions in this libary) will return an empty list.

!!! warning "Entries *up to* 1999th"
    If you try to access over the 1999th entry you won't get *up to* 1999 entries,
    you'll get an empty list.

For example, this will get you entries 1990 - 1999 - a 9 element list of [`MediaEntry`]
[simplejustwatchapi.tuples.MediaEntry],
as expected:

```python
from simplejustwatchapi import search

results = search("title", count=9, offset=1990)
# len(results) == 9, as expected.
```

But trying to get 1990 - 2000 will result in an empty list:

```python
from simplejustwatchapi import search

results = search("title", count=10, offset=1990)
# len(results) == 0, API responded with empty list.
```

Overshooting will also result in an empty list:

```python
from simplejustwatchapi import search

results = search("title", count=100, offset=1950)
# len(results) == 0, API responded with empty list.
```

Interestingly, you'll still hit [too high operation complexity](#operation-complexity)
for too high values of `count`, even though you'd get an empty list anyway:

```python
from simplejustwatchapi import search

results = search("title", count=200, offset=1950)
# Errors out due to complexity.
```



## Getting more results and pagination

This library allows for very simple pagination in
[`search`][simplejustwatchapi.justwatch.search] and
[`popular`][simplejustwatchapi.justwatch.popular] commands through `count` and `offset`
arguments. The first one configures how many entries are returned in one request, the
second allows for offsetting which is the "first" result (thus "skipping" first
entries).

This lets you get around issues with [operation complexity](#operation-complexity)
and get more data. For example, to get all available popular titles without running
into the issue with complexity you can:

```python
from simplejustwatchapi import popular

i = 0
page = 99
all_results = []
while results := popular(count=page, offset=i):
    i += page
    all_results.extend(results)
# len(all_results) == 1980
```
While trying to get them all at once will result in an exception:
```python
from simplejustwatchapi import popular

results = popular(count=1980)
# JustWatchApiError is raised due to too high operation complexity.
```

Unfortunately, I don't know of any way around the issue with
[maximum number of entries](#maximum-number-of-entries), so it's impossible to get more
than 1999 elements.

!!! note "Stability of results with pagination"
    All "pagination" is done on the side of the API by offsetting which is the first
    element. Since this operation isn't keeping any context between requests there's no
    guarantee of "stability" of results between requests - whether titles will shift
    order while you're getting pages.



## Provider codes

!!! tip "Different countries can have different codes"
    The codes can be different for different countries. For example, "Amazon Prime
    Video" in US has code `amp`, but in France it's `prv`. At the same time "Netflix"
    seems to always be `nfx`.

!!! note "Invalid codes provide no filtering"
    If you try to use invalid/unexpected codes for a given country then **no filtering
    will be done at all**. There will be no internal errors, or exceptions; functions
    will return normal values, rather than some kind of empty response.

### [`providers`][simplejustwatchapi.justwatch.providers] function

The easiest way of getting all provider codes for filtering in
[`search`][simplejustwatchapi.justwatch.search] and
[`popular`][simplejustwatchapi.justwatch.popular] functions
is through [`providers`][simplejustwatchapi.justwatch.providers] function, for example:

```python
from simplejustwatchapi import popular, providers

codes = [
    package.short_name
    for package
    # Look up all providers in the UK:
    in providers("GB")
    # Only get codes for specific providers:
    if package.name in ("Netflix", "Amazon Prime Video")
]

# codes == ["nfx", "amp"]

# Get popular titles only for selected providers:
popular_netflix_amazon = popular(providers=codes)
```


### Query parameters from JustWatch

You can also get them by going to [JustWatch main page](https://www.justwatch.com/)
and selecting **at least 2** of available services. **You need 2**, for 1 you'll get its
full name. Only for multiple you'll get the needed codes as
`?providers=<code1>+<code2>+...` query parameter. For example on US version the URL when
selecting "Netflix" and "Amazon Prime Video" is:

```url
https://www.justwatch.com/us?providers=amp,nfx
```

So the codes for them are `amp` and `nfx` for the US.


### Stored output from other functions

The codes are also returned when looking up offers (through pretty much any function
aside from [`providers`][simplejustwatchapi.justwatch.providers]) through
[`OfferPackage`][simplejustwatchapi.tuples.OfferPackage] and its `short_name` field.
For example, to get the codes from [`search`][simplejustwatchapi.justwatch.search]:

```python
from simplejustwatchapi import popular, search

search_results = search("The Matrix", "US", "en", 5, True)
name_to_code_dict = {
    # Get name and short_name/code from packages:
    offer.package.name: offer.package.short_name
    for entry in search_results  # Iterate all entries.
    for offer in entry.offers  # Iterate all offers per entry.
}
# Keep country code the same between functions, as different countries might have
# different provider codes.
# Also, "providers" needs to be a list, not a dict.
popular_results = popular("US", providers=list(name_to_code_dict.values()))
```

!!! tip "When this actually might be useful"
    This only makes sense if you are already using other functions. To get **just** the
    codes use the [`providers`](#providers-function) function instead.
