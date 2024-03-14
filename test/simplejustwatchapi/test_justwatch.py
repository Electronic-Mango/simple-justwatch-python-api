from unittest.mock import MagicMock, patch
from pytest import fixture

from simplejustwatchapi.justwatch import search, details

JUSTWATCH_GRAPHQL_URL = "https://apis.justwatch.com/graphql"
SEARCH_INPUT = ("TITLE", "COUNTRY", "LANGUAGE", 5, True)
DETAILS_INPUT = ("NODE ID", "COUNTRY", "LANGUAGE", False)
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
def test_search(requests_mock, parser_mock, httpx_post_mock) -> None:
    results = search(*SEARCH_INPUT)
    requests_mock.assert_called_with(*SEARCH_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == DUMMY_ENTRIES


@patch("simplejustwatchapi.justwatch.parse_details_response", return_value=DUMMY_ENTRIES)
@patch("simplejustwatchapi.justwatch.prepare_details_request", return_value=DUMMY_REQUEST)
def test_details(requests_mock, parser_mock, httpx_post_mock) -> None:
    results = details(*DETAILS_INPUT)
    requests_mock.assert_called_with(*DETAILS_INPUT)
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == DUMMY_ENTRIES
