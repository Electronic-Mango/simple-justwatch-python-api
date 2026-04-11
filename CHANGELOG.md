# Changelog

## 1.0.0

I don't really know what would it mean for this project to reach 1.0.0/stable, so here it is anyways.

Change error handling - add new exceptions instead of asserts:
 - `JustWatchHttpError` - API responded with a non-`2xx` status code
 - `JustWatchApiError` - response from API has errors in JSON
 - `JustWatchError` - parent for all other exceptions for easier catching

Add a lot more comprehensive documentation, created with Zensical.

## 0.19.0

Change license to MIT.

## 0.18.2

Update "Usage" in README.md so it's up to date on PyPi page.

## 0.18.1

Update README.md ToC so it's up to date on PyPi page.
Also added missing unit tests.

## 0.18.0

Add two new functions:

- `popular` - looking up currently popular titles
- `providers` - get data about service providers (like "Netflix") to use in filtering in `popular` or `search`

`popular` and `search` allows for basic pagination with `offset` parameter.

`search` can now be used without specified `title`, making it oddly similar to `popular`, but oh well. I figured it out after `popular` was ready.

## 0.17.1

Apparently, even it's discouraged according to PEP 639, it's still needed to get correct license on PyPi.

## 0.17

Add two new functions - one for seasons and one for episodes.
They allow for getting more granular information - offers for individual seasons, or episodes; rather than show as a whole.

## 0.16

Query for:
 - scoring (IMDB, TMDB, Rotten Tomatoes, JustWatch)
 - JustWatch likes and dislikes
 - JustWatch charts/ranks
 - age certification

## 0.15

Add TMDB ID to responses.
Remove default `element_count`, if not found in API response use `None`.

## 0.14

Add 2 new commands:

`details` - look up details for a single entry by its node ID
`offers_for_countries` - look up offers for a single entry by its node ID, allows for specifying multiple countries

## 0.13

Add "short_description" to API response, matching "showDescription" field in GraphQL API.

## 0.12

Update data structures and media formats in README.md.

## 0.11

Add "runtime" field.

## 0.10

Update poster type hint to include "None".

## 0.9

Fix issue where GraphQL API didn't return poster URL, now in this situation this API will set "None" as poster.
Specify offer icon format to "PNG". Previously it would leave "{format}" in offer icon URL.

## 0.8

Add example response to README.md.

## 0.7

Fix auto-generated docs.

## 0.6

Combine parser and requests module, add more docstrings.

## 0.5

Rename main module to `simplejustwatchapi`.

## 0.4

Minor fixes.

## 0.3

Fix IMDb URL type hint, fix poster and entry URL.

## 0.1

Initial release.
