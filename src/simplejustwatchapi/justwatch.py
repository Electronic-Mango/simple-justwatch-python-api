"""Main module orchestrating requests to JustWatch GraphQL API.
Currently only search requests are supported.
"""

from httpx import post

from simplejustwatchapi.query import (
    MediaEntry,
    parse_details_response,
    parse_search_response,
    prepare_details_request,
    prepare_search_request,
)

_GRAPHQL_API_URL = "https://apis.justwatch.com/graphql"


def search(
    title: str, country: str = "US", language: str = "en", count: int = 4, best_only: bool = True
) -> list[MediaEntry]:
    """Search JustWatch for given title.
    Returns a list of entries up to ``count``.
    ``best_only`` allows filtering out redundant offers, e.g. when if provide offers service
    in 4K, HD and SD, using ``best_only = True`` returns only 4K option, ``best_only = False``
    returns all three.

    Args:
        title: title to search
        country: country to search for offers, ``US`` by default
        language: language of responses, ``en`` by default
        count: how many responses should be returned
        best_only: return only best offers if ``True``, return all offers if ``False``

    Returns:
        List of ``MediaEntry`` NamedTuples parsed from JustWatch response
    """
    request = prepare_search_request(title, country, language, count, best_only)
    response = post(_GRAPHQL_API_URL, json=request)
    response.raise_for_status()
    return parse_search_response(response.json())


def details(
    node_id: str, country: str = "US", language: str = "en", best_only: bool = True
) -> MediaEntry:
    """Get details of entry for a given ID.
    ``best_only`` allows filtering out redundant offers, e.g. when if provide offers service
    in 4K, HD and SD, using ``best_only = True`` returns only 4K option, ``best_only = False``
    returns all three.

    Args:
        node_id: ID of entry to look up
        country: country to search for offers, ``US`` by default
        language: language of responses, ``en`` by default
        best_only: return only best offers if ``True``, return all offers if ``False``

    Returns:
        MediaEntry NamedTuple with data about requested entry.
    """
    request = prepare_details_request(node_id, country, language, best_only)
    response = post(_GRAPHQL_API_URL, json=request)
    response.raise_for_status()
    return parse_details_response(response.json())
