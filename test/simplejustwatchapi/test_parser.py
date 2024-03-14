from pytest import mark

from simplejustwatchapi.query import MediaEntry, Offer, parse_search_response, OfferPackage, parse_details_response

DETAILS_URL = "https://justwatch.com"
IMAGES_URL = "https://images.justwatch.com"

RESPONSE_NODE_1 = {
    "id": "id1",
    "objectId": 1,
    "objectType": "MOVIE",
    "content": {
        "title": "title 1",
        "fullPath": "/full/path/1/",
        "originalReleaseYear": 2000,
        "originalReleaseDate": "21-06-2000",
        "runtime": 123,
        "shortDescription": "Movie 1 description",
        "genres": [{"shortName": "gen1"}, {"shortName": "gen2"}],
        "externalIds": {"imdbId": "imdbId1"},
        "posterUrl": "/poster/url/1.jpg",
        "backdrops": [
            {"backdropUrl": "/back/drop/url/1.jpg"},
            {"backdropUrl": "/back/drop/url/2.jpg"},
        ],
    },
    "offers": [
        {
            "id": "OFFER ID 1",
            "monetizationType": "MON_TYPE_1",
            "presentationType": "HD",
            "retailPrice": "$19.99",
            "retailPriceValue": 19.99,
            "currency": "USD",
            "lastChangeRetailPriceValue": 9.99,
            "type": "SOME_TYPE_1",
            "package": {
                "id": "id1",
                "packageId": 1,
                "clearName": "Service 1",
                "technicalName": "service1",
                "icon": "/icon/url/service1",
            },
            "standardWebURL": "www.service1.com/offer/url/1/",
            "elementCount": 123,
            "availableTo": "2100-07-15",
            "deeplinkRoku": "/link/to/roku/service1",
            "subtitleLanguages": ["sub_lang_1", "sub_lang_2", "sub_lang_3"],
            "videoTechnology": ["GOOD_ONE", "BAD_ONE", "IDK"],
            "audioTechnology": ["ALSO_GOOD_ONE", "ALSO_BAD_ONE", "ALSO_IDK"],
            "audioLanguages": ["lang_1", "lang_2", "lang_3"],
        },
        {
            "id": "OFFER ID 2",
            "monetizationType": "MON_TYPE_1",
            "presentationType": "SD",
            "retailPrice": "$9.99",
            "retailPriceValue": 9.99,
            "currency": "USD",
            "lastChangeRetailPriceValue": 4.99,
            "type": "SOME_TYPE_2",
            "package": {
                "id": "id2",
                "packageId": 2,
                "clearName": "Service 2",
                "technicalName": "service2",
                "icon": "/icon/url/service2",
            },
            "standardWebURL": "www.service1.com/offer/url/2/",
            "elementCount": 456,
            "availableTo": "2100-04-12",
            "deeplinkRoku": "/link/to/roku/service2",
            "subtitleLanguages": ["sub_lang_4", "sub_lang_5"],
            "videoTechnology": ["BAD_ONE", "IDK"],
            "audioTechnology": ["ALSO_BAD_ONE", "ALSO_IDK"],
            "audioLanguages": ["lang_4", "lang_5"],
        },
    ],
}
PARSED_NODE_1 = MediaEntry(
    "id1",
    1,
    "MOVIE",
    "title 1",
    DETAILS_URL + "/full/path/1/",
    2000,
    "21-06-2000",
    123,
    "Movie 1 description",
    ["gen1", "gen2"],
    "imdbId1",
    IMAGES_URL + "/poster/url/1.jpg",
    [IMAGES_URL + "/back/drop/url/1.jpg", IMAGES_URL + "/back/drop/url/2.jpg"],
    [
        Offer(
            "OFFER ID 1",
            "MON_TYPE_1",
            "HD",
            "$19.99",
            19.99,
            "USD",
            9.99,
            "SOME_TYPE_1",
            OfferPackage(
                "id1",
                1,
                "Service 1",
                "service1",
                IMAGES_URL + "/icon/url/service1",
            ),
            "www.service1.com/offer/url/1/",
            123,
            "2100-07-15",
            "/link/to/roku/service1",
            ["sub_lang_1", "sub_lang_2", "sub_lang_3"],
            ["GOOD_ONE", "BAD_ONE", "IDK"],
            ["ALSO_GOOD_ONE", "ALSO_BAD_ONE", "ALSO_IDK"],
            ["lang_1", "lang_2", "lang_3"],
        ),
        Offer(
            "OFFER ID 2",
            "MON_TYPE_1",
            "SD",
            "$9.99",
            9.99,
            "USD",
            4.99,
            "SOME_TYPE_2",
            OfferPackage(
                "id2",
                2,
                "Service 2",
                "service2",
                IMAGES_URL + "/icon/url/service2",
            ),
            "www.service1.com/offer/url/2/",
            456,
            "2100-04-12",
            "/link/to/roku/service2",
            ["sub_lang_4", "sub_lang_5"],
            ["BAD_ONE", "IDK"],
            ["ALSO_BAD_ONE", "ALSO_IDK"],
            ["lang_4", "lang_5"],
        ),
    ],
)

RESPONSE_NODE_2 = {
    "id": "id2",
    "objectId": 2,
    "objectType": "TV SHOW",
    "content": {
        "title": "title 2",
        "fullPath": "/full/path/2/",
        "originalReleaseYear": 2010,
        "originalReleaseDate": "11-01-2010",
        "runtime": 456,
        "shortDescription": "TV show 2 description",
        "genres": [{"shortName": "gen2"}, {"shortName": "gen3"}],
        "externalIds": {"imdbId": "imdbId2"},
        "posterUrl": "/poster/url/2.jpg",
        "backdrops": [
            {"backdropUrl": "/back/drop/url/3.jpg"},
        ],
    },
    "offers": [
        {
            "id": "offer_id_3",
            "monetizationType": "MON_TYPE_3",
            "presentationType": "_4K",
            "retailPrice": "£199.9",
            "retailPriceValue": 199.9,
            "currency": "GBP",
            "lastChangeRetailPriceValue": 399.99,
            "type": "SOME_TYPE_3",
            "package": {
                "id": "id3",
                "packageId": 3,
                "clearName": "Service 3",
                "technicalName": "service3",
                "icon": "/icon/url/service3",
            },
            "standardWebURL": "www.service3.com/offer/url/1/",
            "elementCount": 0,
            "availableTo": None,
            "deeplinkRoku": None,
            "subtitleLanguages": ["sub_lang_4"],
            "videoTechnology": ["BAD_ONE"],
            "audioTechnology": ["ALSO_BAD_ONE"],
            "audioLanguages": ["lang_4"],
        },
    ],
}
PARSED_NODE_2 = MediaEntry(
    "id2",
    2,
    "TV SHOW",
    "title 2",
    DETAILS_URL + "/full/path/2/",
    2010,
    "11-01-2010",
    456,
    "TV show 2 description",
    ["gen2", "gen3"],
    "imdbId2",
    IMAGES_URL + "/poster/url/2.jpg",
    [IMAGES_URL + "/back/drop/url/3.jpg"],
    [
        Offer(
            "offer_id_3",
            "MON_TYPE_3",
            "_4K",
            "£199.9",
            199.9,
            "GBP",
            399.99,
            "SOME_TYPE_3",
            OfferPackage(
                "id3",
                3,
                "Service 3",
                "service3",
                IMAGES_URL + "/icon/url/service3",
            ),
            "www.service3.com/offer/url/1/",
            0,
            None,
            None,
            ["sub_lang_4"],
            ["BAD_ONE"],
            ["ALSO_BAD_ONE"],
            ["lang_4"],
        ),
    ],
)
RESPONSE_NODE_3 = {
    "id": "id3",
    "objectId": 3,
    "objectType": "OTHER",
    "content": {
        "title": "title 3",
        "fullPath": "/full/path/3/",
        "originalReleaseYear": 2020,
        "originalReleaseDate": "12-02-2020",
        "runtime": 123,
        "posterUrl": "/poster/url/3.jpg",
    },
}
PARSED_NODE_3 = MediaEntry(
    "id3",
    3,
    "OTHER",
    "title 3",
    DETAILS_URL + "/full/path/3/",
    2020,
    "12-02-2020",
    123,
    None,
    [],
    None,
    IMAGES_URL + "/poster/url/3.jpg",
    [],
    [],
)

API_SEARCH_RESPONSE_JSON = {
    "data": {
        "popularTitles": {
            "edges": [
                {"node": RESPONSE_NODE_1},
                {"node": RESPONSE_NODE_2},
                {"node": RESPONSE_NODE_3},
            ]
        }
    }
}

API_SEARCH_RESPONSE_NO_DATA = {"data": {"popularTitles": {"edges": []}}}


@mark.parametrize(
    argnames=["response_json", "expected_output"],
    argvalues=[
        (API_SEARCH_RESPONSE_JSON, [PARSED_NODE_1, PARSED_NODE_2, PARSED_NODE_3]),
        (API_SEARCH_RESPONSE_NO_DATA, [])
    ]
)
def test_parse_search_response(response_json, expected_output) -> None:
    parsed_entries = parse_search_response(response_json)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=["response_json", "expected_output"],
    argvalues=[
        ({"data": {"node": RESPONSE_NODE_1}}, PARSED_NODE_1),
        ({"data": {"node": RESPONSE_NODE_2}}, PARSED_NODE_2),
        ({"data": {"node": RESPONSE_NODE_3}}, PARSED_NODE_3),
        ({"errors": [], "data": {"node": None}}, None)
    ]
)
def test_parse_details_response(response_json, expected_output) -> None:
    parsed_entries = parse_details_response(response_json)
    assert parsed_entries == expected_output
