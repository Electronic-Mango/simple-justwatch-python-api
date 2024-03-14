"""Main module orchestrating requests to JustWatch GraphQL API.
Currently supported requests are:
 - ``search`` - search for entries via title
 - ``details`` - get details for given node ID
 - ``offers_for_countries`` - get all offers for entry with given node ID,
   can look for offers for multiple countries
"""

from httpx import post

from simplejustwatchapi.query import (
    MediaEntry,
    Offer,
    parse_details_response,
    parse_offers_for_countries_response,
    parse_search_response,
    prepare_details_request,
    prepare_offers_for_countries_request,
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
        ``MediaEntry`` NamedTuple with data about requested entry.
    """
    request = prepare_details_request(node_id, country, language, best_only)
    response = post(_GRAPHQL_API_URL, json=request)
    response.raise_for_status()
    return parse_details_response(response.json())


def offers_for_countries(
    node_id: str, countries: set[str], language: str = "en", best_only: bool = True
) -> dict[str, list[Offer]]:
    """Get offers for entry of given node ID for all countries passed as argument.
    Language argument only specifies format of price string, e.g. whether ".", or "," is used
    in decimal fractions.

    Returned dict has keys matching "countries" argument and values are list of found offers.
    If no countries are passed (an empty set given as argument) empty dict is returned.

    Country codes passed as argument are case-insensitive, however keys in returned dict will match
    them exactly. E.g. for countries specified as:
    .. code-block:: python

        {"uK", "Us", "AU", "ca"}

    returned dict will have the following structure:
    .. code-block:: python

        {
            "uK": [... offers ...],
            "Us": [... offers ...],
            "AU": [... offers ...],
            "ca": [... offers ...],
        }

    ``best_only`` allows filtering out redundant offers, e.g. when if provide offers service
    in 4K, HD and SD, using ``best_only = True`` returns only 4K option, ``best_only = False``
    returns all three.

    Args:
        node_id: ID of entry to look up offers for
        countries: set of country codes to search for offers
        language: language of responses, ``en`` by default
        best_only: return only best offers if ``True``, return all offers if ``False``

    Returns:
        ``dict`` where keys match values in ``countries`` and keys are all found offers for their
        respective countries
    """
    if not countries:
        return {}
    request = prepare_offers_for_countries_request(node_id, countries, language, best_only)
    response = post(_GRAPHQL_API_URL, json=request)
    response.raise_for_status()
    return parse_offers_for_countries_response(response.json(), countries)
