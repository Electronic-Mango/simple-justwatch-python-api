from unittest.mock import MagicMock, patch

from pytest import fixture, mark, raises

from simplejustwatchapi.exceptions import JustWatchHttpError
from simplejustwatchapi.justwatch import (
    details,
    episodes,
    offers_for_countries,
    popular,
    providers,
    search,
    seasons,
)

JUSTWATCH_GRAPHQL_URL = "https://apis.justwatch.com/graphql"

SEARCH_INPUT = ("TITLE", "COUNTRY", "LANGUAGE", 5, True, 10, ["prov1", "prov2"])
POPULAR_INPUT = ("COUNTRY", "LANGUAGE", 5, True, 10, ["prov1", "prov2"])
DETAILS_INPUT = ("NODE ID", "COUNTRY", "LANGUAGE", False)
OFFERS_COUNTRIES_INPUT = {"COUNTRY1", "COUNTRY2", "COUNTRY3"}
OFFERS_INPUT = ("NODE ID", OFFERS_COUNTRIES_INPUT, "LANGUAGE", True)
PROVIDERS_INPUT = "US"

DUMMY_REQUEST = {"dummy": "request"}
DUMMY_RESPONSE = {"dummy": "response"}
DUMMY_ENTRIES = [MagicMock(), MagicMock(), None]


@fixture
def post_mock_success(mocker):
    post_mock = mocker.patch("simplejustwatchapi.justwatch.post")
    post_mock.return_value.json.return_value = DUMMY_RESPONSE
    post_mock.return_value.is_success = True
    yield post_mock
    post_mock.assert_called_with(JUSTWATCH_GRAPHQL_URL, json=DUMMY_REQUEST)


@fixture
def post_mock_failure(mocker):
    post_mock = mocker.patch("simplejustwatchapi.justwatch.post")
    post_mock.return_value.is_success = False
    return post_mock


@patch("simplejustwatchapi.justwatch.parse_search_response", return_value=DUMMY_ENTRIES)
@patch("simplejustwatchapi.justwatch.prepare_search_request", return_value=DUMMY_REQUEST)
def test_search(requests_mock, parser_mock, post_mock_success):
    results = search(*SEARCH_INPUT)
    requests_mock.assert_called_with(*SEARCH_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == DUMMY_ENTRIES


@patch("simplejustwatchapi.justwatch.parse_popular_response", return_value=DUMMY_ENTRIES)
@patch("simplejustwatchapi.justwatch.prepare_popular_request", return_value=DUMMY_REQUEST)
def test_popular(requests_mock, parser_mock, post_mock_success):
    results = popular(*POPULAR_INPUT)
    requests_mock.assert_called_with(*POPULAR_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == DUMMY_ENTRIES


@patch("simplejustwatchapi.justwatch.parse_details_response")
@patch("simplejustwatchapi.justwatch.prepare_details_request", return_value=DUMMY_REQUEST)
@mark.parametrize("parse_results", [DUMMY_ENTRIES, None])
def test_details(requests_mock, parser_mock, parse_results, post_mock_success):
    parser_mock.return_value = parse_results
    results = details(*DETAILS_INPUT)
    requests_mock.assert_called_with(*DETAILS_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == parse_results


@patch("simplejustwatchapi.justwatch.parse_seasons_response")
@patch("simplejustwatchapi.justwatch.prepare_seasons_request", return_value=DUMMY_REQUEST)
@mark.parametrize("parse_results", [DUMMY_ENTRIES, None])
def test_seasons(requests_mock, parser_mock, parse_results, post_mock_success):
    parser_mock.return_value = parse_results
    results = seasons(*DETAILS_INPUT)
    requests_mock.assert_called_with(*DETAILS_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == parse_results


@patch("simplejustwatchapi.justwatch.parse_episodes_response")
@patch("simplejustwatchapi.justwatch.prepare_episodes_request", return_value=DUMMY_REQUEST)
@mark.parametrize("parse_results", [DUMMY_ENTRIES, None])
def test_episodes(requests_mock, parser_mock, parse_results, post_mock_success):
    parser_mock.return_value = parse_results
    results = episodes(*DETAILS_INPUT)
    requests_mock.assert_called_with(*DETAILS_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == parse_results


@patch(
    "simplejustwatchapi.justwatch.parse_offers_for_countries_response", return_value=DUMMY_ENTRIES
)
@patch(
    "simplejustwatchapi.justwatch.prepare_offers_for_countries_request", return_value=DUMMY_REQUEST
)
def test_offers_for_countries(requests_mock, parser_mock, post_mock_success):
    results = offers_for_countries(*OFFERS_INPUT)
    requests_mock.assert_called_with(*OFFERS_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE, OFFERS_COUNTRIES_INPUT)
    assert results == DUMMY_ENTRIES


@patch("simplejustwatchapi.justwatch.parse_offers_for_countries_response")
@patch("simplejustwatchapi.justwatch.prepare_offers_for_countries_request")
@patch("simplejustwatchapi.justwatch.post")
def test_offers_for_countries_returns_empty_dict_for_empty_countries_set(
    requests_mock, parser_mock, post_mock_success
):
    results = offers_for_countries("", set(), "", False)
    assert not results
    requests_mock.assert_not_called()
    parser_mock.assert_not_called()
    post_mock_success.assert_not_called()


@patch("simplejustwatchapi.justwatch.parse_providers_response", return_value=DUMMY_ENTRIES)
@patch("simplejustwatchapi.justwatch.prepare_providers_request", return_value=DUMMY_REQUEST)
def test_providers(requests_mock, parser_mock, post_mock_success):
    results = providers(PROVIDERS_INPUT)
    requests_mock.assert_called_with(PROVIDERS_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == DUMMY_ENTRIES


@mark.parametrize(
    argnames=("prepare_name", "function", "inputs"),
    argvalues=[
        ("prepare_search_request", search, SEARCH_INPUT),
        ("prepare_popular_request", popular, POPULAR_INPUT),
        ("prepare_details_request", details, DETAILS_INPUT),
        ("prepare_seasons_request", seasons, DETAILS_INPUT),
        ("prepare_episodes_request", episodes, DETAILS_INPUT),
        ("prepare_offers_for_countries_request", offers_for_countries, OFFERS_INPUT),
        ("prepare_providers_request", providers, (PROVIDERS_INPUT,)),
    ],
)
def test_search_raises_http_error(prepare_name, function, inputs, post_mock_failure):
    full_mock_name = f"simplejustwatchapi.justwatch.{prepare_name}"
    with patch(full_mock_name), raises(JustWatchHttpError):
        function(*inputs)
