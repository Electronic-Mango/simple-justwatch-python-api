from unittest.mock import patch

from pytest import mark, raises

from simplejustwatchapi.exceptions import JustWatchError
from simplejustwatchapi.query import (
    prepare_details_request,
    prepare_episodes_request,
    prepare_offers_for_countries_request,
    prepare_popular_request,
    prepare_providers_request,
    prepare_search_request,
    prepare_seasons_request,
)

DUMMY_SEARCH_QUERY = "A DUMMY SEARCH QUERY"
DUMMY_POPULAR_QUERY = "A DUMMY POPULAR QUERY"
DUMMY_DETAILS_QUERY = "A DUMMY DETAILS QUERY"
DUMMY_SEASONS_QUERY = "A DUMMY SEASONS QUERY"
DUMMY_EPISODES_QUERY = "A DUMMY EPISODES QUERY"
DUMMY_OFFERS_FOR_COUNTRIES_QUERY = "A DUMMY OFFERS FOR COUNTRIES QUERY"
DUMMY_PROVIDERS_QUERY = "A DUMMY PROVIDERS QUERY"


def common_variables(best_only):
    return {
        "formatPoster": "JPG",
        "formatOfferIcon": "PNG",
        "profile": "S718",
        "backdropProfile": "S1920",
        "filter": {"bestOnly": best_only},
    }


def locale_variables(country, language):
    return {
        "country": country.upper(),
        "language": language,
    }


@patch("simplejustwatchapi.query.GRAPHQL_SEARCH_QUERY", DUMMY_SEARCH_QUERY)
@mark.parametrize(
    argnames=(
        "title",
        "country",
        "language",
        "count",
        "best_only",
        "offset",
        "providers",
    ),
    argvalues=[
        ("TITLE 1", "US", "en", 5, True, 0, ""),
        ("TITLE 2", "gb", "fr", 10, False, 20, ["provider1", "provider2"]),
        ("TITLE 3", "fr", "de-SWITZ123", 20, True, 20, "provider3"),
        ("TITLE 4", "it", "ro-HELLO123", 30, True, 30, []),
        ("TITLE 5", "dk", "us", 40, True, 40, None),
    ],
)
def test_prepare_search_request(
    title,
    country,
    language,
    count,
    best_only,
    offset,
    providers,
):
    expected_request = {
        "operationName": "GetSearchTitles",
        "variables": {
            "first": count,
            "searchTitlesFilter": {"searchQuery": title, "packages": providers},
            **common_variables(best_only),
            **locale_variables(country, language),
            "offset": offset or None,
        },
        "query": DUMMY_SEARCH_QUERY,
    }
    request = prepare_search_request(
        title, country, language, count, best_only, offset, providers
    )
    assert expected_request == request


@patch("simplejustwatchapi.query.GRAPHQL_POPULAR_QUERY", DUMMY_POPULAR_QUERY)
@mark.parametrize(
    argnames=("country", "language", "count", "best_only", "offset", "providers"),
    argvalues=[
        ("US", "en-123ASD", 5, True, 0, ""),
        ("gb", "fr", 10, False, 20, ["provider1", "provider2"]),
        ("fr", "de-FGH76", 20, True, 20, "provider3"),
        ("it", "ro", 30, True, 30, []),
        ("dk", "us", 40, True, 40, None),
    ],
)
def test_prepare_popular_request(
    country,
    language,
    count,
    best_only,
    offset,
    providers,
):
    expected_request = {
        "operationName": "GetPopularTitles",
        "variables": {
            "first": count,
            "popularTitlesFilter": {"packages": providers},
            **common_variables(best_only),
            **locale_variables(country, language),
            "offset": offset or None,
        },
        "query": DUMMY_POPULAR_QUERY,
    }
    request = prepare_popular_request(
        country, language, count, best_only, offset, providers
    )
    assert expected_request == request


@patch("simplejustwatchapi.query.GRAPHQL_DETAILS_QUERY", DUMMY_DETAILS_QUERY)
@mark.parametrize(
    argnames=("node_id", "country", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", "US", "en", True),
        ("NODE ID 1", "gb", "fr-213SD45", False),
    ],
)
def test_prepare_details_request(node_id, country, language, best_only):
    expected_request = {
        "operationName": "GetTitleNode",
        "variables": {
            "nodeId": node_id,
            **common_variables(best_only),
            **locale_variables(country, language),
        },
        "query": DUMMY_DETAILS_QUERY,
    }
    request = prepare_details_request(node_id, country, language, best_only)
    assert expected_request == request


@patch("simplejustwatchapi.query.GRAPHQL_SEASONS_QUERY", DUMMY_SEASONS_QUERY)
@mark.parametrize(
    argnames=("node_id", "country", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", "US", "en", True),
        ("NODE ID 1", "gb", "fr", False),
    ],
)
def test_prepare_seasons_request(node_id, country, language, best_only):
    expected_request = {
        "operationName": "GetTitleNode",
        "variables": {
            "nodeId": node_id,
            **common_variables(best_only),
            **locale_variables(country, language),
        },
        "query": DUMMY_SEASONS_QUERY,
    }
    request = prepare_seasons_request(node_id, country, language, best_only)
    assert expected_request == request


@patch("simplejustwatchapi.query.GRAPHQL_EPISODES_QUERY", DUMMY_EPISODES_QUERY)
@mark.parametrize(
    argnames=("node_id", "country", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", "US", "en", True),
        ("NODE ID 1", "gb", "fr", False),
    ],
)
def test_prepare_episodes_request(node_id, country, language, best_only):
    expected_request = {
        "operationName": "GetTitleNode",
        "variables": {
            "nodeId": node_id,
            **common_variables(best_only),
            **locale_variables(country, language),
        },
        "query": DUMMY_EPISODES_QUERY,
    }
    request = prepare_episodes_request(node_id, country, language, best_only)
    assert expected_request == request


@patch(
    "simplejustwatchapi.query.graphql_offers_for_countries_query",
    return_value=DUMMY_OFFERS_FOR_COUNTRIES_QUERY,
)
@mark.parametrize(
    argnames=("node_id", "countries", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", {"US"}, "en", True),
        ("NODE ID 2", {"au"}, "fr", False),
        ("NODE ID 3", {"gb", "US", "Ca"}, "de-GER123", True),
    ],
)
def test_prepare_offers_for_countries_request(
    _, node_id, countries, language, best_only
):
    expected_request = {
        "operationName": "GetTitleOffers",
        "variables": {
            "nodeId": node_id,
            "language": language,
            **common_variables(best_only),
        },
        "query": DUMMY_OFFERS_FOR_COUNTRIES_QUERY,
    }
    request = prepare_offers_for_countries_request(
        node_id, countries, language, best_only
    )
    assert expected_request == request


@patch(
    "simplejustwatchapi.query.GRAPHQL_PROVIDERS_QUERY",
    DUMMY_PROVIDERS_QUERY,
)
@mark.parametrize(
    argnames="country",
    argvalues=["US", "gb", "fR", "It"],
)
def test_prepare_providers_request(country):
    expected_request = {
        "operationName": "GetProviders",
        "variables": {
            "country": country.upper(),
            "formatOfferIcon": "PNG",
        },
        "query": DUMMY_PROVIDERS_QUERY,
    }
    request = prepare_providers_request(country)
    assert expected_request == request


def test_prepare_offers_for_countries_request_asserts_on_empty_countries_set():
    expected_error_message = "No country codes, should not happen!"
    with raises(JustWatchError) as error:
        prepare_offers_for_countries_request("", set(), "en", True)
    assert str(error.value) == expected_error_message
