from re import match
from unittest.mock import patch

from pytest import mark, raises

from simplejustwatchapi.exceptions import (
    JustWatchCountryCodeError,
    JustWatchError,
)
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


@patch("simplejustwatchapi.query.graphql_search_query", return_value=DUMMY_SEARCH_QUERY)
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
        ("TITLE 1", "US", "language 1", 5, True, 0, ""),
        ("TITLE 2", "gb", "language 2", 10, False, 20, ["provider1", "provider2"]),
        ("TITLE 3", "fr", "language 3", 20, True, 20, "provider3"),
        ("TITLE 4", "it", "language 4", 30, True, 30, []),
        ("TITLE 5", "dk", "language 5", 40, True, 40, None),
    ],
)
def test_prepare_search_request(
    _,
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
    request = prepare_search_request(
        title, country, language, count, best_only, offset, providers
    )
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
    query_mock, invalid_code
):
    expected_error_message = (
        f"Invalid country code: {invalid_code}, it must be 2 characters long!"
    )
    with raises(JustWatchCountryCodeError) as error:
        prepare_search_request("", invalid_code, "", 1, True, 2, None)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()


@patch(
    "simplejustwatchapi.query.graphql_popular_query", return_value=DUMMY_POPULAR_QUERY
)
@mark.parametrize(
    argnames=("country", "language", "count", "best_only", "offset", "providers"),
    argvalues=[
        ("US", "language 1", 5, True, 0, ""),
        ("gb", "language 2", 10, False, 20, ["provider1", "provider2"]),
        ("fr", "language 3", 20, True, 20, "provider3"),
        ("it", "language 4", 30, True, 30, []),
        ("dk", "language 5", 40, True, 40, None),
    ],
)
def test_prepare_popular_request(
    _,
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
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
            "offset": offset or None,
        },
        "query": DUMMY_POPULAR_QUERY,
    }
    request = prepare_popular_request(
        country, language, count, best_only, offset, providers
    )
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
def test_prepare_popular_request_asserts_on_invalid_country_code(
    query_mock, invalid_code
):
    expected_error_message = (
        f"Invalid country code: {invalid_code}, it must be 2 characters long!"
    )
    with raises(JustWatchCountryCodeError) as error:
        prepare_popular_request(invalid_code, "", 1, True, 2, None)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()


@patch(
    "simplejustwatchapi.query.graphql_details_query", return_value=DUMMY_DETAILS_QUERY
)
@mark.parametrize(
    argnames=("node_id", "country", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", "US", "language 1", True),
        ("NODE ID 1", "gb", "language 2", False),
    ],
)
def test_prepare_details_request(_, node_id, country, language, best_only):
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
    query_mock, invalid_code
):
    expected_error_message = (
        f"Invalid country code: {invalid_code}, it must be 2 characters long!"
    )
    with raises(JustWatchCountryCodeError) as error:
        prepare_details_request("", invalid_code, "", True)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()


@patch(
    "simplejustwatchapi.query.graphql_seasons_query", return_value=DUMMY_SEASONS_QUERY
)
@mark.parametrize(
    argnames=("node_id", "country", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", "US", "language 1", True),
        ("NODE ID 1", "gb", "language 2", False),
    ],
)
def test_prepare_seasons_request(_, node_id, country, language, best_only):
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
    query_mock, invalid_code
):
    expected_error_message = (
        f"Invalid country code: {invalid_code}, it must be 2 characters long!"
    )
    with raises(JustWatchCountryCodeError) as error:
        prepare_seasons_request("", invalid_code, "", True)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()


@patch(
    "simplejustwatchapi.query.graphql_episodes_query", return_value=DUMMY_EPISODES_QUERY
)
@mark.parametrize(
    argnames=("node_id", "country", "language", "best_only"),
    argvalues=[
        ("NODE ID 1", "US", "language 1", True),
        ("NODE ID 1", "gb", "language 2", False),
    ],
)
def test_prepare_episodes_request(_, node_id, country, language, best_only):
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
    query_mock, invalid_code
):
    expected_error_message = (
        f"Invalid country code: {invalid_code}, it must be 2 characters long!"
    )
    with raises(JustWatchCountryCodeError) as error:
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
    _, node_id, countries, language, best_only
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

    request = prepare_offers_for_countries_request(
        node_id, countries, language, best_only
    )

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
    query_mock, codes, invalid_code_regex
):
    expected_error_message = (
        rf"Invalid country code: ({invalid_code_regex}), it must be 2 characters long!"
    )
    with raises(JustWatchCountryCodeError) as error:
        prepare_offers_for_countries_request("", codes, "", True)
    # Regex here is required, as sets are unordered,
    # so we have no guarantee which code will fail first.
    assert match(expected_error_message, str(error.value))
    query_mock.assert_not_called()


@patch("simplejustwatchapi.query.graphql_offers_for_countries_query")
def test_prepare_offers_for_countries_request_asserts_on_empty_countries_set(
    query_mock,
):
    expected_error_message = "No country codes, should not happen!"
    with raises(JustWatchError) as error:
        prepare_offers_for_countries_request("", set(), "", True)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()


@patch(
    "simplejustwatchapi.query.graphql_providers_query",
    return_value=DUMMY_PROVIDERS_QUERY,
)
@mark.parametrize(
    argnames=("country"),
    argvalues=["US", "gb", "fR", "It"],
)
def test_prepare_providers_request(_, country):
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


@patch("simplejustwatchapi.query.graphql_search_query")
@mark.parametrize(
    argnames="invalid_code",
    argvalues=[
        "United Stated of America",  # too long
        "usa",  # too long
        "u",  # too short
    ],
)
def test_prepare_providers_request_asserts_on_invalid_country_code(
    query_mock, invalid_code
):
    expected_error_message = (
        f"Invalid country code: {invalid_code}, it must be 2 characters long!"
    )
    with raises(JustWatchCountryCodeError) as error:
        prepare_providers_request(invalid_code)
    assert str(error.value) == expected_error_message
    query_mock.assert_not_called()
