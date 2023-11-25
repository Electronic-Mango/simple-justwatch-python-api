from simplejustwatchpythonapi.parser import MediaEntry, Offer, parse_search_response

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
            "monetizationType": "MON_TYPE_1",
            "presentationType": "HD",
            "standardWebURL": "www.service1.com/offer/url/1/",
            "retailPrice": "$19.99",
            "retailPriceValue": 19.99,
            "currency": "USD",
            "package": {
                "clearName": "Service 1",
                "technicalName": "service1",
                "icon": "/icon/url/service1",
            },
        },
        {
            "monetizationType": "MON_TYPE_1",
            "presentationType": "SD",
            "standardWebURL": "www.service1.com/offer/url/1/",
            "retailPrice": "$9.99",
            "retailPriceValue": 9.99,
            "currency": "USD",
            "package": {
                "clearName": "Service 1",
                "technicalName": "service1",
                "icon": "/icon/url/service1",
            },
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
    ["gen1", "gen2"],
    "imdbId1",
    IMAGES_URL + "/poster/url/1.jpg",
    [IMAGES_URL + "/back/drop/url/1.jpg", IMAGES_URL + "/back/drop/url/2.jpg"],
    [
        Offer(
            "MON_TYPE_1",
            "HD",
            "www.service1.com/offer/url/1/",
            "$19.99",
            19.99,
            "USD",
            "Service 1",
            "service1",
            IMAGES_URL + "/icon/url/service1",
        ),
        Offer(
            "MON_TYPE_1",
            "SD",
            "www.service1.com/offer/url/1/",
            "$9.99",
            9.99,
            "USD",
            "Service 1",
            "service1",
            IMAGES_URL + "/icon/url/service1",
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
        "genres": [{"shortName": "gen2"}, {"shortName": "gen3"}],
        "externalIds": {"imdbId": "imdbId2"},
        "posterUrl": "/poster/url/2.jpg",
        "backdrops": [
            {"backdropUrl": "/back/drop/url/3.jpg"},
        ],
    },
    "offers": [
        {
            "monetizationType": "MON_TYPE_3",
            "presentationType": "_4K",
            "standardWebURL": "www.service2.com/offer/url/2/",
            "retailPrice": "£199.9",
            "retailPriceValue": 199.9,
            "currency": "GBP",
            "package": {
                "clearName": "Service 2",
                "technicalName": "service2",
                "icon": "/icon/url/service2",
            },
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
    ["gen2", "gen3"],
    "imdbId2",
    IMAGES_URL + "/poster/url/2.jpg",
    [IMAGES_URL + "/back/drop/url/3.jpg"],
    [
        Offer(
            "MON_TYPE_3",
            "_4K",
            "www.service2.com/offer/url/2/",
            "£199.9",
            199.9,
            "GBP",
            "Service 2",
            "service2",
            IMAGES_URL + "/icon/url/service2",
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
    [],
    None,
    IMAGES_URL + "/poster/url/3.jpg",
    [],
    [],
)

API_RESPONSE_JSON = {
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


def test_parse() -> None:
    parsed_entries = parse_search_response(API_RESPONSE_JSON)
    assert [PARSED_NODE_1, PARSED_NODE_2, PARSED_NODE_3] == parsed_entries
