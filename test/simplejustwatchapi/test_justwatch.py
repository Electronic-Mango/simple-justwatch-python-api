from unittest.mock import MagicMock, patch

from simplejustwatchapi.justwatch import search

JUSTWATCH_GRAPHQL_URL = "https://apis.justwatch.com/graphql"
SEARCH_INPUT = ("TITLE", "COUNTRY", "LANGUAGE", 5, True)
DUMMY_REQUEST = {"dummy": "request"}
DUMMY_RESPONSE = {"dummy": "response"}
DUMMY_ENTRIES = [MagicMock(), MagicMock(), None]


@patch("simplejustwatchapi.justwatch.post")
@patch("simplejustwatchapi.justwatch.parse_search_response", return_value=DUMMY_ENTRIES)
@patch("simplejustwatchapi.justwatch.prepare_search_request", return_value=DUMMY_REQUEST)
def test_search(requests_mock, parser_mock, httpx_mock) -> None:
    httpx_mock().json.return_value = DUMMY_RESPONSE

    results = search(*SEARCH_INPUT)

    requests_mock.assert_called_with(*SEARCH_INPUT)
    httpx_mock.assert_called_with(JUSTWATCH_GRAPHQL_URL, json=DUMMY_REQUEST)
    httpx_mock().raise_for_status.assert_called()
    parser_mock.assert_called_with(DUMMY_RESPONSE)
    assert results == DUMMY_ENTRIES
