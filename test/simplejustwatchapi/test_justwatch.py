from unittest.mock import MagicMock, patch

from pytest import fixture

from simplejustwatchapi.justwatch import details, offers_for_countries, search

JUSTWATCH_GRAPHQL_URL = "https://apis.justwatch.com/graphql"

SEARCH_INPUT = ("TITLE", "COUNTRY", "LANGUAGE", 5, True)
DETAILS_INPUT = ("NODE ID", "COUNTRY", "LANGUAGE", False)
OFFERS_COUNTRIES_INPUT = {"COUNTRY1", "COUNTRY2", "COUNTRY3"}
OFFERS_INPUT = ("NODE ID", OFFERS_COUNTRIES_INPUT, "LANGUAGE", True)

DUMMY_REQUEST = {"dummy": "request"}
DUMMY_RESPONSE = {"dummy": "response"}
DUMMY_ENTRIES = [MagicMock(), MagicMock(), None]


@fixture()
def httpx_post_mock(mocker):
    post_mock = mocker.patch("simplejustwatchapi.justwatch.post")
    post_mock.return_value.json.return_value = DUMMY_RESPONSE
    yield post_mock
    post_mock.assert_called_with(JUSTWATCH_GRAPHQL_URL, json=DUMMY_REQUEST)
    post_mock.return_value.raise_for_status.assert_called()


@patch("simplejustwatchapi.justwatch.parse_search_response", return_value=DUMMY_ENTRIES)
@patch("simplejustwatchapi.justwatch.prepare_search_request", return_value=DUMMY_REQUEST)
def test_search(requests_mock, parser_mock, httpx_post_mock):
    results = search(*SEARCH_INPUT)
    requests_mock.assert_called_with(*SEARCH_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == DUMMY_ENTRIES


@patch("simplejustwatchapi.justwatch.parse_details_response", return_value=DUMMY_ENTRIES)
@patch("simplejustwatchapi.justwatch.prepare_details_request", return_value=DUMMY_REQUEST)
def test_details(requests_mock, parser_mock, httpx_post_mock):
    results = details(*DETAILS_INPUT)
    requests_mock.assert_called_with(*DETAILS_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == DUMMY_ENTRIES


@patch(
    "simplejustwatchapi.justwatch.parse_offers_for_countries_response", return_value=DUMMY_ENTRIES
)
@patch(
    "simplejustwatchapi.justwatch.prepare_offers_for_countries_request", return_value=DUMMY_REQUEST
)
def test_offers_for_countries(requests_mock, parser_mock, httpx_post_mock):
    results = offers_for_countries(*OFFERS_INPUT)
    requests_mock.assert_called_with(*OFFERS_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE, OFFERS_COUNTRIES_INPUT)
    assert results == DUMMY_ENTRIES


def test_offers_for_countries_returns_empty_dict_for_empty_countries_set():
    results = offers_for_countries("", set(), "", False)
    assert not results
