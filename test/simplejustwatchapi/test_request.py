from re import match
from unittest.mock import MagicMock, patch

from pytest import mark, raises

from simplejustwatchapi.query import (
    prepare_details_request,
    prepare_episodes_request,
    prepare_offers_for_countries_request,
    prepare_search_request,
    prepare_seasons_request,
)

DUMMY_SEARCH_QUERY = "A DUMMY SEARCH QUERY"
DUMMY_DETAILS_QUERY = "A DUMMY DETAILS QUERY"
DUMMY_SEASONS_QUERY = "A DUMMY SEASONS QUERY"
DUMMY_EPISODES_QUERY = "A DUMMY EPISODES QUERY"
DUMMY_OFFERS_FOR_COUNTRIES_QUERY = "A DUMMY OFFERS FOR COUNTRIES QUERY"


@patch("simplejustwatchapi.query.graphql_search_query", return_value=DUMMY_SEARCH_QUERY)
@mark.parametrize(
    argnames=("title", "country", "language", "count", "best_only", "offset"),
    argvalues=[
        ("TITLE 1", "US", "language 1", 5, True, 0),
        ("TITLE 2", "gb", "language 2", 10, False, 20),
    ],
)
def test_prepare_search_request(
    _,
    title: str,
    country: str,
    language: str,
    count: int,
    best_only: bool,
    offset: int,
):
    expected_request = {
        "operationName": "GetSearchTitles",
        "variables": {
            "first": count,
            "searchTitlesFilter": {"searchQuery": title},
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
            "offset": offset or None,
        },
        "query": DUMMY_SEARCH_QUERY,
    }
    request = prepare_search_request(title, country, language, count, best_only, offset)
    assert expected_request == request


@patch("simplejustwatchapi.query.graphql_search_query")
@mark.parametrize(
    argnames="invalid_code",
    argvalues=[
        "United Stated of America",  # too long
        "usa",  # too long
        "u",  # too short
    ],
)
def test_prepare_search_request_asserts_on_invalid_country_code(
    query_mock: MagicMock, invalid_code: str
):
    expected_error_message = f"Invalid country code: {invalid_code}, code must be 2 characters long"
    with raises(AssertionError) as error:
        prepare_search_request("", invalid_code, "", 1, True, 2)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()


@patch("simplejustwatchapi.query.graphql_details_query", return_value=DUMMY_DETAILS_QUERY)
@mark.parametrize(
    argnames=("node_id", "country", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", "US", "language 1", True),
        ("NODE ID 1", "gb", "language 2", False),
    ],
)
def test_prepare_details_request(_, node_id: str, country: str, language: str, best_only: bool):
    expected_request = {
        "operationName": "GetTitleNode",
        "variables": {
            "nodeId": node_id,
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": DUMMY_DETAILS_QUERY,
    }
    request = prepare_details_request(node_id, country, language, best_only)
    assert expected_request == request


@patch("simplejustwatchapi.query.graphql_details_query")
@mark.parametrize(
    argnames="invalid_code",
    argvalues=[
        "United Stated of America",  # too long
        "usa",  # too long
        "u",  # too short
    ],
)
def test_prepare_details_request_asserts_on_invalid_country_code(
    query_mock: MagicMock, invalid_code: str
):
    expected_error_message = f"Invalid country code: {invalid_code}, code must be 2 characters long"
    with raises(AssertionError) as error:
        prepare_details_request("", invalid_code, "", True)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()


@patch("simplejustwatchapi.query.graphql_seasons_query", return_value=DUMMY_SEASONS_QUERY)
@mark.parametrize(
    argnames=("node_id", "country", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", "US", "language 1", True),
        ("NODE ID 1", "gb", "language 2", False),
    ],
)
def test_prepare_seasons_request(_, node_id: str, country: str, language: str, best_only: bool):
    expected_request = {
        "operationName": "GetTitleNode",
        "variables": {
            "nodeId": node_id,
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": DUMMY_SEASONS_QUERY,
    }
    request = prepare_seasons_request(node_id, country, language, best_only)
    assert expected_request == request


@patch("simplejustwatchapi.query.graphql_seasons_query")
@mark.parametrize(
    argnames="invalid_code",
    argvalues=[
        "United Stated of America",  # too long
        "usa",  # too long
        "u",  # too short
    ],
)
def test_prepare_seasons_request_asserts_on_invalid_country_code(
    query_mock: MagicMock, invalid_code: str
):
    expected_error_message = f"Invalid country code: {invalid_code}, code must be 2 characters long"
    with raises(AssertionError) as error:
        prepare_seasons_request("", invalid_code, "", True)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()


@patch("simplejustwatchapi.query.graphql_episodes_query", return_value=DUMMY_EPISODES_QUERY)
@mark.parametrize(
    argnames=("node_id", "country", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", "US", "language 1", True),
        ("NODE ID 1", "gb", "language 2", False),
    ],
)
def test_prepare_episodes_request(_, node_id: str, country: str, language: str, best_only: bool):
    expected_request = {
        "operationName": "GetTitleNode",
        "variables": {
            "nodeId": node_id,
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": DUMMY_EPISODES_QUERY,
    }
    request = prepare_episodes_request(node_id, country, language, best_only)
    assert expected_request == request


@patch("simplejustwatchapi.query.graphql_episodes_query")
@mark.parametrize(
    argnames="invalid_code",
    argvalues=[
        "United Stated of America",  # too long
        "usa",  # too long
        "u",  # too short
    ],
)
def test_prepare_episodes_request_asserts_on_invalid_country_code(
    query_mock: MagicMock, invalid_code: str
):
    expected_error_message = f"Invalid country code: {invalid_code}, code must be 2 characters long"
    with raises(AssertionError) as error:
        prepare_episodes_request("", invalid_code, "", True)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()


@patch(
    "simplejustwatchapi.query.graphql_offers_for_countries_query",
    return_value=DUMMY_OFFERS_FOR_COUNTRIES_QUERY,
)
@mark.parametrize(
    argnames=("node_id", "countries", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", {"US"}, "language 1", True),
        ("NODE ID 2", {"au"}, "language 2", False),
        ("NODE ID 3", {"gb", "US", "Ca"}, "language 3", True),
    ],
)
def test_prepare_offers_for_countries_request(
    _, node_id: str, countries: set[str], language: str, best_only: bool
):
    expected_request = {
        "operationName": "GetTitleOffers",
        "variables": {
            "nodeId": node_id,
            "language": language,
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": DUMMY_OFFERS_FOR_COUNTRIES_QUERY,
    }

    request = prepare_offers_for_countries_request(node_id, countries, language, best_only)

    assert expected_request == request


@patch("simplejustwatchapi.query.graphql_offers_for_countries_query")
@mark.parametrize(
    argnames=("codes", "invalid_code_regex"),
    argvalues=[
        ({"United Stated of America", "UK"}, "United Stated of America"),  # too long
        ({"uk", "usa"}, "usa"),  # too long
        ({"canada", "uk", "usa"}, r"usa|canada"),  # too long
        ({"u", "uK", "a"}, r"a|u"),  # too short
        ({"A"}, "A"),  # too short
    ],
)
def test_prepare_offers_for_countries_request_asserts_on_invalid_country_codes(
    query_mock: MagicMock, codes: set[str], invalid_code_regex: set[str]
):
    expected_error_message = (
        rf"Invalid country code: ({invalid_code_regex}), code must be 2 characters long"
    )
    with raises(AssertionError) as error:
        prepare_offers_for_countries_request("", codes, "", True)
    # Regex here is required, as sets are unordered,
    # so we have no guarantee which code will fail first.
    assert match(expected_error_message, str(error.value))
    query_mock.assert_not_called()


@patch("simplejustwatchapi.query.graphql_offers_for_countries_query")
def test_prepare_offers_for_countries_request_asserts_on_empty_countries_set(query_mock: MagicMock):
    expected_error_message = "Cannot prepare offers request without specified countries"
    with raises(AssertionError) as error:
        prepare_offers_for_countries_request("", set(), "", True)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()
