"""
Main functions used for obtaining data from JustWatch GraphQL API.

Each function sends **one** GraphQL query to JustWatch API and returns API response
parsed into a [`NamedTuple`][typing.NamedTuple] from [`tuples`]
[simplejustwatchapi.tuples] module. Everything is handled on the API side through
prepared GraphQL query.

Most functions have a number of common arguments (in addition to function-specific)
ones, like `node_id`, or `title` to search for):

| Name        | Description |
|-------------|-------------|
| `country`   | 2-letter country code for which offers will be returned, e.g., `US`, \
                `GB`, `DE`. |
| `language`  | Language code for responses' language. It can be just basic 2-letter \
                code (e.g., `en`, `de`) or with a BCP47-like suffix (e.g., `en-US`, \
                `de-CH`). I don't think this is exactly BCP47, as the suffix can \
                contain only uppercase letters and numbers. |
| `best_only` | Whether to return only "best" offers for each provider instead of, \
                e.g., separate offer for SD, HD, and 4K. |

Functions returning data for multiple titles
([`search`][simplejustwatchapi.justwatch.search],
[`details`][simplejustwatchapi.justwatch.details])
also allow for specifying number of elements, basic pagination, and filtering for
specific providers:

| Name        | Description |
|-------------|-------------|
| `count`     | How many entries should be returned. |
| `offset`    | Basic "pagination", how many first elements should be skipped. \
                Everything is handled on API side, this library isn't doing any \
                filtering. |
| `providers` | Providers (like Netflix, Amazon Prime Video) for which offers should \
                returned. Requires 3-letter "short name". Check \
                [`providers`][simplejustwatchapi.justwatch.providers] for an example \
                of how you can get that value.

Each function can raise two exceptions:

| Exception | Cause |
|-----------|-------|
| [`JustWatchHttpError`][simplejustwatchapi.exceptions.JustWatchHttpError] | \
    JustWatch API responded with non-`2xx` code. |
| [`JustWatchApiError`][simplejustwatchapi.exceptions.JustWatchApiError] | \
    JSON response from JustWatch API contains errors. If this exception is raised, \
    then API responded with `2xx` code |
"""

from httpx import post

from simplejustwatchapi.exceptions import JustWatchHttpError
from simplejustwatchapi.query import (
    parse_details_response,
    parse_episodes_response,
    parse_offers_for_countries_response,
    parse_popular_response,
    parse_providers_response,
    parse_search_response,
    parse_seasons_response,
    prepare_details_request,
    prepare_episodes_request,
    prepare_offers_for_countries_request,
    prepare_popular_request,
    prepare_providers_request,
    prepare_search_request,
    prepare_seasons_request,
)
from simplejustwatchapi.tuples import Episode, MediaEntry, Offer, OfferPackage

_GRAPHQL_API_URL = "https://apis.justwatch.com/graphql"


def search(
    title: str = "",
    country: str = "US",
    language: str = "en",
    count: int = 4,
    best_only: bool = True,
    offset: int = 0,
    providers: list[str] | str | None = None,
) -> list[MediaEntry]:
    """
    Search JustWatch for the given title.

    If no `title` is provided (or an empty string, as per default value) you'll get a
    selection of "popular" titles. Without `title` the output is very similar to
    [`popular`][simplejustwatchapi.justwatch.popular] function. This argument isn't
    stripped, so passing string with only spaces will look for those spaces.

    `country` is a 2-letter country code for which offers are selected. It should be
    uppercase, however it will be normalized to uppercase automatically. It **must** be
    2-letters long. It looks like ISO 3166-1 alpha-2 standard, however API doesn't
    specify exact standard. If unexpected code is used, then [`JustWatchApiError`]
    [simplejustwatchapi.exceptions.JustWatchApiError] exception is raised, as the API
    will respond with internal error.

    `language` is a language code for language in response (e.g., description, title).
    It's value isn't normalized and **must** be provided in expected format, including
    case. It looks like a subset of IETF BCP 47, however the suffix can contain only
    uppercase letters and numbers. It can be a simple 2-letter code (e.g., `en`, `de`),
    it can also contain optional suffix (e.g., `en-US`, `de-CH`).

    Returns a list of entries up to `count`.

    `offset` specifies how many first entries should be skipped. This is done on API
    side, not the library side; the returned list is still directly parsed from API
    response. I'm not sure if it guarantees stability of results - it repeated calls to
    this function with increasing offset will guarantee that you won't get repeats.

    JustWatch API won't allow for getting more than 2000 responses, either through
    `count`, or when `count + offset` is equal or greater than 2000 - it will return an
    empty list instead (ALWAYS an empty list, if `offset` is lower than 2000 it won't
    include entries up to 2000).

    `best_only` allows filtering out redundant offers, e.g. when service provides offers
    in 4K, HD and SD, using `best_only = True` returns only 4K option,
    `best_only = False` returns all three.

    `providers` is a list of (usually) 3-letter service identifiers (e.g, `nfx` for
    "Netflix). Only entries which are available for given providers will be returned.
    For single provider you can either pass a single string, or a list of one string.
    For `None` (also the default value) entries for all providers will be looked up.
    Invalid names will be ignored, however if all are invalid, then no filtering will be
    done. You can look up values through [`providers`]
    [simplejustwatchapi.justwatch.providers] function.

    Args:
        title (str): Title to search, empty string by default.
        country (str): Country to search for offers, `US` by default.
        language (str): Language of responses, `en` by default.
        count (int): How many responses should be returned.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.
        offset (int): Search results offset.
        providers (list[str] | str | None): 3-letter service identifier(s),
            or `None` for all providers.

    Returns:
        (list[MediaEntry]): List of tuples parsed from JustWatch response.

    Raises:
        exceptions.JustWatchApiError: JSON response from API has internal errors.
        exceptions.JustWatchHttpError: JustWatch API didn't respond with `2xx` code.

    """
    request = prepare_search_request(
        title, country, language, count, best_only, offset, providers
    )
    response = _post_to_jw_graphql_api(request)
    return parse_search_response(response)


def popular(
    country: str = "US",
    language: str = "en",
    count: int = 4,
    best_only: bool = True,
    offset: int = 0,
    providers: list[str] | str | None = None,
) -> list[MediaEntry]:
    """
    Look up all currently popular titles on JustWatch.

    This function returns similar values as `search` with no `title` provided.

    `country` is a 2-letter country code for which offers are selected. It should be
    uppercase, however it will be normalized to uppercase automatically. It **must** be
    2-letters long. It looks like ISO 3166-1 alpha-2 standard, however API doesn't
    specify exact standard. If unexpected code is used, then [`JustWatchApiError`]
    [simplejustwatchapi.exceptions.JustWatchApiError] exception is raised, as the API
    will respond with internal error.

    `language` is a language code for language in response (e.g., description, title).
    It's value isn't normalized and **must** be provided in expected format, including
    case. It looks like a subset of IETF BCP 47, however the suffix can contain only
    uppercase letters and numbers. It can be a simple 2-letter code (e.g., `en`, `de`),
    it can also contain optional suffix (e.g., `en-US`, `de-CH`).

    Returns a list of entries up to `count`.

    `offset` specifies how many first entries should be skipped. This is done on API
    side, not the library side; the returned list is still directly parsed from API
    response. I'm not sure if it guarantees stability of results - whether repeated
    calls to this function with increasing offset will guarantee that you won't get
    repeats.

    JustWatch API won't allow for getting more than 2000 responses, either through
    `count`, or when `count + offset` is equal or greater than 2000 - it will return an
    empty list instead (ALWAYS an empty list, if `offset` is lower than 2000 it won't
    include entries up to 2000).

    `best_only` allows filtering out redundant offers, e.g. when service provides offers
    in 4K, HD and SD, using `best_only = True` returns only 4K option,
    `best_only = False` returns all three.

    `providers` is a list of (usually) 3-letter service identifiers (e.g, `nfx` for
    "Netflix). Only entries which are available for given providers will be returned.
    For single provider you can either pass a single string, or a list of one string.
    For `None` (also the default value) entries for all providers will be looked up.
    Invalid names will be ignored, however if all are invalid, then no filtering will be
    done. You can look up values through [`providers`]
    [simplejustwatchapi.justwatch.providers] function.

    Args:
        country (str): Country to search for offers, `US` by default.
        language (str): Language of responses, `en` by default.
        count (int): How many responses should be returned.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.
        offset (int): Search results offset.
        providers (list[str] | str | None): 3-letter service identifier(s),
            or `None` for all providers.

    Returns:
        (list[MediaEntry]): List of tuples parsed from JustWatch response.

    Raises:
        exceptions.JustWatchApiError: JSON response from API has internal errors.
        exceptions.JustWatchHttpError: JustWatch API didn't respond with `2xx` code.

    """
    request = prepare_popular_request(
        country, language, count, best_only, offset, providers
    )
    response = _post_to_jw_graphql_api(request)
    return parse_popular_response(response)


def details(
    node_id: str,
    country: str = "US",
    language: str = "en",
    best_only: bool = True,
) -> MediaEntry:
    """
    Get details of entry for a given ID.

    `country` is a 2-letter country code for which offers are selected. It should be
    uppercase, however it will be normalized to uppercase automatically. It **must** be
    2-letters long. It looks like ISO 3166-1 alpha-2 standard, however API doesn't
    specify exact standard. If unexpected code is used, then [`JustWatchApiError`]
    [simplejustwatchapi.exceptions.JustWatchApiError] exception is raised, as the API
    will respond with internal error.

    `language` is a language code for language in response (e.g., description, title).
    It's value isn't normalized and **must** be provided in expected format, including
    case. It looks like a subset of IETF BCP 47, however the suffix can contain only
    uppercase letters and numbers. It can be a simple 2-letter code (e.g., `en`, `de`),
    it can also contain optional suffix (e.g., `en-US`, `de-CH`).

    `best_only` allows filtering out redundant offers, e.g. when if provide offers
    service in 4K, HD and SD, using `best_only = True` returns only 4K option,
    `best_only = False` returns all three.

    Args:
        node_id (str): ID of entry to look up.
        country (str): Country to search for offers, `US` by default.
        language (str): Language of responses, `en` by default.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.

    Returns:
        (MediaEntry): Tuple with data about requested entry.

    Raises:
        exceptions.JustWatchApiError: JSON response from API has internal errors.
        exceptions.JustWatchHttpError: JustWatch API didn't respond with `2xx` code.

    """
    request = prepare_details_request(node_id, country, language, best_only)
    response = _post_to_jw_graphql_api(request)
    return parse_details_response(response)


def seasons(
    show_id: str, country: str = "US", language: str = "en", best_only: bool = True
) -> list[MediaEntry]:
    """
    Get details of all seasons available for a given show ID.

    `country` is a 2-letter country code for which offers are selected. It should be
    uppercase, however it will be normalized to uppercase automatically. It **must** be
    2-letters long. It looks like ISO 3166-1 alpha-2 standard, however API doesn't
    specify exact standard. If unexpected code is used, then [`JustWatchApiError`]
    [simplejustwatchapi.exceptions.JustWatchApiError] exception is raised, as the API
    will respond with internal error.

    `language` is a language code for language in response (e.g., description, title).
    It's value isn't normalized and **must** be provided in expected format, including
    case. It looks like a subset of IETF BCP 47, however the suffix can contain only
    uppercase letters and numbers. It can be a simple 2-letter code (e.g., `en`, `de`),
    it can also contain optional suffix (e.g., `en-US`, `de-CH`).

    `best_only` allows filtering out redundant offers, e.g. when if provide offers
    service in 4K, HD and SD, using `best_only = True` returns only 4K option,
    `best_only = False` returns all three.

    Args:
        show_id (str): ID of show to look up seasons for.
        country (str): Country to search for offers, `US` by default.
        language (str): Language of responses, `en` by default.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.

    Returns:
        (list[MediaEntry]): List of tuples with seasons data about requested entry.

    Raises:
        exceptions.JustWatchApiError: JSON response from API has internal errors.
        exceptions.JustWatchHttpError: JustWatch API didn't respond with `2xx` code.

    """
    request = prepare_seasons_request(show_id, country, language, best_only)
    response = _post_to_jw_graphql_api(request)
    return parse_seasons_response(response)


def episodes(
    season_id: str, country: str = "US", language: str = "en", best_only: bool = True
) -> list[Episode]:
    """
    Get details of all episodes available for a given season ID.

    `country` is a 2-letter country code for which offers are selected. It should be
    uppercase, however it will be normalized to uppercase automatically. It **must** be
    2-letters long. It looks like ISO 3166-1 alpha-2 standard, however API doesn't
    specify exact standard. If unexpected code is used, then [`JustWatchApiError`]
    [simplejustwatchapi.exceptions.JustWatchApiError] exception is raised, as the API
    will respond with internal error.

    `language` is a language code for language in response (e.g., description, title).
    It's value isn't normalized and **must** be provided in expected format, including
    case. It looks like a subset of IETF BCP 47, however the suffix can contain only
    uppercase letters and numbers. It can be a simple 2-letter code (e.g., `en`, `de`),
    it can also contain optional suffix (e.g., `en-US`, `de-CH`).

    `best_only` allows filtering out redundant offers, e.g. when if provide offers
    service in 4K, HD and SD, using `best_only = True` returns only 4K option,
    `best_only = False` returns all three.

    Args:
        season_id (str): ID of season to look up episodes for.
        country (str): Country to search for offers, `US` by default.
        language (str): Language of responses, `en` by default.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.

    Returns:
        (list[Episode]): List of tuples with episode data about requested entry.

    Raises:
        exceptions.JustWatchApiError: JSON response from API has internal errors.
        exceptions.JustWatchHttpError: JustWatch API didn't respond with `2xx` code.

    """
    request = prepare_episodes_request(season_id, country, language, best_only)
    response = _post_to_jw_graphql_api(request)
    return parse_episodes_response(response)


def offers_for_countries(
    node_id: str,
    countries: set[str],
    language: str = "en",
    best_only: bool = True,
) -> dict[str, list[Offer]]:
    """
    Get offers for entry of given node ID for all countries passed as argument.

    `countries` is a set of 2-letter country codes. They all should be uppercase,
    however it will be normalized to uppercase automatically. They **must** be
    2-letters long. It looks like ISO 3166-1 alpha-2 standard, however API doesn't
    specify exact standard. If unexpected codes are used, then [`JustWatchApiError`]
    [simplejustwatchapi.exceptions.JustWatchApiError] exception is raised, as the API
    will respond with internal error.

    `language` is a language code for language in response (e.g., description, title).
    It's value isn't normalized and **must** be provided in expected format, including
    case. It looks like a subset of IETF BCP 47, however the suffix can contain only
    uppercase letters and numbers. It can be a simple 2-letter code (e.g., `en`, `de`),
    it can also contain optional suffix (e.g., `en-US`, `de-CH`).

    Returned dict has keys matching `countries` argument and values are list of found
    offers. If no countries are passed (an empty set given as argument) empty dict is
    returned.

    Country codes passed as argument are case-insensitive, however keys in returned dict
    will match them exactly. For example, for countries specified as:

    ```python
    {"uK", "Us", "AU", "ca"}
    ```

    returned dict will have the following structure:

    ```python
    {
        "uK": [ ... offers ... ],
        "Us": [ ... offers ... ],
        "AU": [ ... offers ... ],
        "ca": [ ... offers ... ],
    }
    ```

    `best_only` allows filtering out redundant offers, e.g. when if provide offers
    service in 4K, HD and SD, using `best_only = True` returns only 4K option,
    `best_only = False` returns all three.

    Args:
        node_id (str): ID of entry to look up offers for.
        countries (set[str]): 2-letter country codes to search for offers.
        language (str): Language of responses, `en` by default.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.

    Returns:
        (dict[str, list[Offer]]): Keys match values in `countries` and values are all
            found offers for their respective countries.

    Raises:
        exceptions.JustWatchApiError: JSON response from API has internal errors.
        exceptions.JustWatchHttpError: JustWatch API didn't respond with `2xx` code.

    """
    if not countries:
        return {}
    request = prepare_offers_for_countries_request(
        node_id, countries, language, best_only
    )
    response = _post_to_jw_graphql_api(request)
    return parse_offers_for_countries_response(response, countries)


def providers(country: str = "US") -> list[OfferPackage]:
    """
    Look up all providers for the given country code.

    `country` is a 2-letter country code for which offers are selected. It should be
    uppercase, however it will be normalized to uppercase automatically. It **must** be
    2-letters long. It looks like ISO 3166-1 alpha-2 standard, however API doesn't
    specify exact standard. If unexpected code is used, then [`JustWatchApiError`]
    [simplejustwatchapi.exceptions.JustWatchApiError] exception is raised, as the API
    will respond with internal error.

    Args:
        country (str): 2-letter country code, `US` by default.

    Returns:
        (list[OfferPackage]): List of all found providers. [`OfferPackage`]
            [simplejustwatchapi.tuples.OfferPackage] tuple matches values in [`Offer`]
            [simplejustwatchapi.tuples.Offer] (and thus in [`MediaEntry`]
            [simplejustwatchapi.tuples.MediaEntry]), but the data structure is the same,
            so the same tuple is reused.

    Raises:
        exceptions.JustWatchApiError: JSON response from API has internal errors.
        exceptions.JustWatchHttpError: JustWatch API didn't respond with `2xx` code.

    """
    request = prepare_providers_request(country)
    response = _post_to_jw_graphql_api(request)
    return parse_providers_response(response)


def _post_to_jw_graphql_api(request_json: dict) -> dict:
    """
    Send a GraphQL query, verify HTTP response, return API response JSON as `dict`.

    Args:
        request_json(dict): JSON with full request - GraphQL query and variables.

    Returns:
        (dict): JSON response from the API.

    Raises:
        exceptions.JustWatchHttpError: JustWatch API didn't respond with `2xx` code.

    """
    response = post(_GRAPHQL_API_URL, json=request_json)
    if not response.is_success:
        raise JustWatchHttpError(response.status_code, response.text)
    return response.json()
