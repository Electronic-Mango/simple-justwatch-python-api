from pytest import mark, raises

from simplejustwatchapi.exceptions import JustWatchApiError
from simplejustwatchapi.query import (
    parse_details_response,
    parse_episodes_response,
    parse_offers_for_countries_response,
    parse_popular_response,
    parse_providers_response,
    parse_search_response,
    parse_seasons_response,
)
from test.simplejustwatchapi.parser_data import (
    API_EPISODES_RESPONSE_JSON,
    API_EPISODES_RESPONSE_NO_DATA,
    API_ERROR_RESPONSE,
    API_SEARCH_RESPONSE_JSON,
    API_SEARCH_RESPONSE_NO_DATA,
    API_SEASONS_RESPONSE_JSON,
    API_SEASONS_RESPONSE_NO_DATA,
    PARSED_EPISODE_1,
    PARSED_EPISODE_2,
    PARSED_EPISODE_3,
    PARSED_NODE_1,
    PARSED_NODE_2,
    PARSED_NODE_3,
    PARSED_PACKAGE_1,
    PARSED_PACKAGE_2,
    PARSED_PACKAGE_3,
    RESPONSE_NODE_1,
    RESPONSE_NODE_2,
    RESPONSE_NODE_3,
    RESPONSE_PACKAGE_1,
    RESPONSE_PACKAGE_2,
    RESPONSE_PACKAGE_3,
)


@mark.parametrize(
    argnames=("response_json", "expected_output"),
    argvalues=[
        (API_SEARCH_RESPONSE_JSON, [PARSED_NODE_1, PARSED_NODE_2, PARSED_NODE_3]),
        (API_SEARCH_RESPONSE_NO_DATA, []),
    ],
)
def test_parse_search_response(response_json, expected_output):
    parsed_entries = parse_search_response(response_json)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=("response_json", "expected_output"),
    argvalues=[
        (API_SEARCH_RESPONSE_JSON, [PARSED_NODE_1, PARSED_NODE_2, PARSED_NODE_3]),
        (API_SEARCH_RESPONSE_NO_DATA, []),
    ],
)
def test_parse_popular_response(response_json, expected_output):
    parsed_entries = parse_popular_response(response_json)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=("response_json", "expected_output"),
    argvalues=[
        ({"data": {"node": RESPONSE_NODE_1}}, PARSED_NODE_1),
        ({"data": {"node": RESPONSE_NODE_2}}, PARSED_NODE_2),
        ({"data": {"node": RESPONSE_NODE_3}}, PARSED_NODE_3),
    ],
)
def test_parse_details_response(response_json, expected_output):
    parsed_entries = parse_details_response(response_json)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=("response_json", "expected_output"),
    argvalues=[
        (API_SEASONS_RESPONSE_JSON, [PARSED_NODE_1, PARSED_NODE_2, PARSED_NODE_3]),
        (API_SEASONS_RESPONSE_NO_DATA, []),
    ],
)
def test_parse_seasons_response(response_json, expected_output):
    parsed_entries = parse_seasons_response(response_json)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=("response_json", "expected_output"),
    argvalues=[
        (
            API_EPISODES_RESPONSE_JSON,
            [PARSED_EPISODE_1, PARSED_EPISODE_2, PARSED_EPISODE_3],
        ),
        (API_EPISODES_RESPONSE_NO_DATA, []),
    ],
)
def test_parse_episodes_response(response_json, expected_output):
    parsed_entries = parse_episodes_response(response_json)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=("response_json", "countries", "expected_output"),
    argvalues=[
        (
            {"data": {"node": {"US": RESPONSE_NODE_1["offers"]}}},
            {"US"},
            {"US": PARSED_NODE_1.offers},
        ),
        (
            {
                "data": {
                    "node": {
                        "US": RESPONSE_NODE_1["offers"],
                        "GB": RESPONSE_NODE_2["offers"],
                    }
                }
            },
            {"US", "GB"},
            {"US": PARSED_NODE_1.offers, "GB": PARSED_NODE_2.offers},
        ),
        (
            {
                "data": {
                    "node": {
                        "US": RESPONSE_NODE_1["offers"],
                        "GB": RESPONSE_NODE_2["offers"],
                    }
                }
            },
            {"US"},
            {"US": PARSED_NODE_1.offers},
        ),
        (
            {
                "data": {
                    "node": {
                        "US": RESPONSE_NODE_1["offers"],
                        "GB": RESPONSE_NODE_2["offers"],
                    }
                }
            },
            {"GB"},
            {"GB": PARSED_NODE_2.offers},
        ),
        (
            {"data": {"node": {"US": RESPONSE_NODE_1["offers"], "GB": []}}},
            {"US", "GB"},
            {"US": PARSED_NODE_1.offers, "GB": []},
        ),
        ({"data": {"node": {"US": []}}}, {"US"}, {"US": []}),
    ],
)
def test_parse_offers_for_countries_response(response_json, countries, expected_output):
    parsed_entries = parse_offers_for_countries_response(response_json, countries)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=("response_json", "expected_output"),
    argvalues=[
        (
            {
                "data": {
                    "packages": [
                        RESPONSE_PACKAGE_1,
                        RESPONSE_PACKAGE_2,
                        RESPONSE_PACKAGE_3,
                    ]
                }
            },
            [PARSED_PACKAGE_1, PARSED_PACKAGE_2, PARSED_PACKAGE_3],
        ),
        ({"data": {"packages": [RESPONSE_PACKAGE_1]}}, [PARSED_PACKAGE_1]),
        ({"data": {"packages": []}}, []),
    ],
)
def test_parse_providers_response(response_json, expected_output):
    parsed_packages = parse_providers_response(response_json)
    assert parsed_packages == expected_output


@mark.parametrize(
    argnames="parse_function",
    argvalues=[
        parse_search_response,
        parse_popular_response,
        parse_details_response,
        parse_seasons_response,
        parse_episodes_response,
        parse_providers_response,
    ],
)
def test_raises_on_internal_api_errors(parse_function):
    with raises(JustWatchApiError):
        parse_function(API_ERROR_RESPONSE)


def test_parse_offers_for_countries_response_raises_on_internal_api_error():
    with raises(JustWatchApiError):
        parse_offers_for_countries_response(API_ERROR_RESPONSE, set())
