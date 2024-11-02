from pytest import mark

from simplejustwatchapi.query import (
    Episode,
    Interactions,
    MediaEntry,
    Offer,
    OfferPackage,
    Scoring,
    Season,
    SeasonsEntry,
    StreamingCharts,
    parse_details_response,
    parse_offers_for_countries_response,
    parse_search_response,
    parse_seasons_response,
)

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
        "externalIds": {"imdbId": "imdbId1", "tmdbId": "tmdbId1"},
        "posterUrl": "/poster/url/1.jpg",
        "backdrops": [
            {"backdropUrl": "/back/drop/url/1.jpg"},
            {"backdropUrl": "/back/drop/url/2.jpg"},
        ],
        "ageCertification": "PG-18",
        "scoring": {
            "imdbScore": 4,
            "imdbVotes": 697,
            "tmdbPopularity": 4.366,
            "tmdbScore": 4.1,
            "tomatoMeter": 75,
            "certifiedFresh": True,
            "jwRating": 0.975424159594,
            "__typename": "Scoring",
        },
        "interactions": {
            "likelistAdditions": 456,
            "dislikelistAdditions": 123,
            "__typename": "InteractionAttributes",
        },
    },
    "streamingCharts": {
        "edges": [
            {
                "streamingChartInfo": {
                    "rank": 79,
                    "trend": "UP",
                    "trendDifference": 40,
                    "topRank": 5,
                    "daysInTop3": 0,
                    "daysInTop10": 5,
                    "daysInTop100": 1632,
                    "daysInTop1000": 3202,
                    "updatedAt": "2024-10-06T05:16:37.603Z",
                    "__typename": "StreamingChartInfo",
                },
                "__typename": "StreamingChartsTitlesEdge",
            }
        ],
        "__typename": "StreamingChartsConnection",
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
    "tmdbId1",
    IMAGES_URL + "/poster/url/1.jpg",
    [IMAGES_URL + "/back/drop/url/1.jpg", IMAGES_URL + "/back/drop/url/2.jpg"],
    "PG-18",
    Scoring(
        4,
        697,
        4.366,
        4.1,
        75,
        True,
        0.975424159594,
    ),
    Interactions(456, 123),
    StreamingCharts(
        79,
        "UP",
        40,
        5,
        0,
        5,
        1632,
        3202,
        "2024-10-06T05:16:37.603Z",
    ),
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
        "externalIds": {"imdbId": "imdbId2", "tmdbId": "tmdbId2"},
        "posterUrl": "/poster/url/2.jpg",
        "backdrops": [
            {"backdropUrl": "/back/drop/url/3.jpg"},
        ],
        "scoring": {
            "imdbScore": 4,
            "imdbVotes": 697,
            "tmdbPopularity": 4.366,
            "tmdbScore": 4.1,
            "tomatoMeter": None,
            "certifiedFresh": None,
            "jwRating": None,
            "__typename": "Scoring",
        },
        "interactions": {
            "likelistAdditions": 1,
            "__typename": "InteractionAttributes",
        },
    },
    "streamingCharts": {
        "edges": None,
        "__typename": "StreamingChartsConnection",
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
    "tmdbId2",
    IMAGES_URL + "/poster/url/2.jpg",
    [IMAGES_URL + "/back/drop/url/3.jpg"],
    None,
    Scoring(
        4,
        697,
        4.366,
        4.1,
        None,
        None,
        None,
    ),
    Interactions(1, None),
    None,
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
    None,
    IMAGES_URL + "/poster/url/3.jpg",
    [],
    None,
    None,
    None,
    None,
    [],
)

PARSED_NODE_4 = SeasonsEntry(
    entry_id="ts85167",
    seasons=[
        Season(
            seasonNumber=1,
            episodes=[
                Episode(seasonNumber=1, episodeNumber=1, title="Pilot"),
                Episode(seasonNumber=1, episodeNumber=2, title="City Council"),
                Episode(seasonNumber=1, episodeNumber=3, title="Werewolf Feud"),
                Episode(seasonNumber=1, episodeNumber=4, title="Manhattan Night Club"),
                Episode(seasonNumber=1, episodeNumber=5, title="Animal Control"),
                Episode(seasonNumber=1, episodeNumber=6, title="Baron's Night Out"),
                Episode(seasonNumber=1, episodeNumber=7, title="The Trial"),
                Episode(seasonNumber=1, episodeNumber=8, title="Citizenship"),
                Episode(seasonNumber=1, episodeNumber=9, title="The Orgy"),
                Episode(seasonNumber=1, episodeNumber=10, title="Ancestry"),
            ],
        ),
        Season(
            seasonNumber=2,
            episodes=[
                Episode(seasonNumber=2, episodeNumber=1, title="Resurrection"),
                Episode(seasonNumber=2, episodeNumber=2, title="Ghosts"),
                Episode(seasonNumber=2, episodeNumber=3, title="Brain Scramblies"),
                Episode(seasonNumber=2, episodeNumber=4, title="The Curse"),
                Episode(seasonNumber=2, episodeNumber=5, title="Colin's Promotion"),
                Episode(seasonNumber=2, episodeNumber=6, title="On the Run"),
                Episode(seasonNumber=2, episodeNumber=7, title="The Return"),
                Episode(seasonNumber=2, episodeNumber=8, title="Collaboration"),
                Episode(seasonNumber=2, episodeNumber=9, title="Witches"),
                Episode(seasonNumber=2, episodeNumber=10, title="Nouveau Théâtre des Vampires"),
            ],
        ),
        Season(
            seasonNumber=3,
            episodes=[
                Episode(seasonNumber=3, episodeNumber=1, title="The Prisoner"),
                Episode(seasonNumber=3, episodeNumber=2, title="The Cloak of Duplication"),
                Episode(seasonNumber=3, episodeNumber=3, title="Gail"),
                Episode(seasonNumber=3, episodeNumber=4, title="The Casino"),
                Episode(seasonNumber=3, episodeNumber=5, title="The Chamber of Judgement"),
                Episode(seasonNumber=3, episodeNumber=6, title="The Escape"),
                Episode(seasonNumber=3, episodeNumber=7, title="The Siren"),
                Episode(seasonNumber=3, episodeNumber=8, title="The Wellness Center"),
                Episode(seasonNumber=3, episodeNumber=9, title="A Farewell"),
                Episode(seasonNumber=3, episodeNumber=10, title="The Portrait"),
            ],
        ),
        Season(
            seasonNumber=4,
            episodes=[
                Episode(seasonNumber=4, episodeNumber=1, title="Reunited"),
                Episode(seasonNumber=4, episodeNumber=2, title="The Lamp"),
                Episode(seasonNumber=4, episodeNumber=3, title="The Grand Opening"),
                Episode(seasonNumber=4, episodeNumber=4, title="The Night Market"),
                Episode(seasonNumber=4, episodeNumber=5, title="Private School"),
                Episode(seasonNumber=4, episodeNumber=6, title="The Wedding"),
                Episode(seasonNumber=4, episodeNumber=7, title="Pine Barrens"),
                Episode(seasonNumber=4, episodeNumber=8, title="Go Flip Yourself"),
                Episode(seasonNumber=4, episodeNumber=9, title="Freddie"),
                Episode(seasonNumber=4, episodeNumber=10, title="Sunrise, Sunset"),
            ],
        ),
        Season(
            seasonNumber=5,
            episodes=[
                Episode(seasonNumber=5, episodeNumber=1, title="The Mall"),
                Episode(seasonNumber=5, episodeNumber=2, title="A Night Out with the Guys"),
                Episode(seasonNumber=5, episodeNumber=3, title="Pride Parade"),
                Episode(seasonNumber=5, episodeNumber=4, title="The Campaign"),
                Episode(seasonNumber=5, episodeNumber=5, title="Local News"),
                Episode(seasonNumber=5, episodeNumber=6, title="Urgent Care"),
                Episode(seasonNumber=5, episodeNumber=7, title="Hybrid Creatures"),
                Episode(seasonNumber=5, episodeNumber=8, title="The Roast"),
                Episode(seasonNumber=5, episodeNumber=9, title="A Weekend at Morrigan Manor"),
                Episode(seasonNumber=5, episodeNumber=10, title="Exit Interview"),
            ],
        ),
        Season(
            seasonNumber=6,
            episodes=[
                Episode(seasonNumber=6, episodeNumber=1, title="Episode 1"),
                Episode(seasonNumber=6, episodeNumber=2, title="Episode 2"),
                Episode(seasonNumber=6, episodeNumber=3, title="Episode 3"),
                Episode(seasonNumber=6, episodeNumber=4, title="Episode 4"),
                Episode(seasonNumber=6, episodeNumber=5, title="Episode 5"),
                Episode(seasonNumber=6, episodeNumber=6, title="Episode 6"),
                Episode(seasonNumber=6, episodeNumber=7, title="Episode 7"),
                Episode(seasonNumber=6, episodeNumber=8, title="Episode 8"),
                Episode(seasonNumber=6, episodeNumber=9, title="Episode 9"),
                Episode(seasonNumber=6, episodeNumber=10, title="Episode 10"),
                Episode(seasonNumber=6, episodeNumber=11, title="Episode 11"),
            ],
        ),
    ],
)
RESPONSE_NODE_4 = {
    "__typename": "Show",
    "id": "ts85167",
    "seasons": [
        {
            "__typename": "Season",
            "content": {"seasonNumber": 1},
            "episodes": [
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 1, "seasonNumber": 1, "title": "Pilot"},
                    "id": "tse1631894",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 2, "seasonNumber": 1, "title": "City Council"},
                    "id": "tse1747980",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 3, "seasonNumber": 1, "title": "Werewolf Feud"},
                    "id": "tse1747981",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 4,
                        "seasonNumber": 1,
                        "title": "Manhattan Night Club",
                    },
                    "id": "tse1747982",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 5, "seasonNumber": 1, "title": "Animal Control"},
                    "id": "tse1747983",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 6,
                        "seasonNumber": 1,
                        "title": "Baron's Night Out",
                    },
                    "id": "tse1769781",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 7, "seasonNumber": 1, "title": "The Trial"},
                    "id": "tse1777016",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 8, "seasonNumber": 1, "title": "Citizenship"},
                    "id": "tse1797942",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 9, "seasonNumber": 1, "title": "The Orgy"},
                    "id": "tse1797943",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 10, "seasonNumber": 1, "title": "Ancestry"},
                    "id": "tse1797944",
                },
            ],
            "id": "tss98319",
        },
        {
            "__typename": "Season",
            "content": {"seasonNumber": 2},
            "episodes": [
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 1, "seasonNumber": 2, "title": "Resurrection"},
                    "id": "tse3177541",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 2, "seasonNumber": 2, "title": "Ghosts"},
                    "id": "tse4343145",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 3, "seasonNumber": 2, "title": "Brain Scramblies"},
                    "id": "tse4366752",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 4, "seasonNumber": 2, "title": "The Curse"},
                    "id": "tse4366760",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 5,
                        "seasonNumber": 2,
                        "title": "Colin's Promotion",
                    },
                    "id": "tse4366763",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 6, "seasonNumber": 2, "title": "On the Run"},
                    "id": "tse4366757",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 7, "seasonNumber": 2, "title": "The Return"},
                    "id": "tse4366754",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 8, "seasonNumber": 2, "title": "Collaboration"},
                    "id": "tse4366751",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 9, "seasonNumber": 2, "title": "Witches"},
                    "id": "tse4366755",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 10,
                        "seasonNumber": 2,
                        "title": "Nouveau Théâtre des " "Vampires",
                    },
                    "id": "tse4366769",
                },
            ],
            "id": "tss200608",
        },
        {
            "__typename": "Season",
            "content": {"seasonNumber": 3},
            "episodes": [
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 1, "seasonNumber": 3, "title": "The Prisoner"},
                    "id": "tse5761373",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 2,
                        "seasonNumber": 3,
                        "title": "The Cloak of Duplication",
                    },
                    "id": "tse5761374",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 3, "seasonNumber": 3, "title": "Gail"},
                    "id": "tse5863479",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 4, "seasonNumber": 3, "title": "The Casino"},
                    "id": "tse5863485",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 5,
                        "seasonNumber": 3,
                        "title": "The Chamber of Judgement",
                    },
                    "id": "tse5863482",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 6, "seasonNumber": 3, "title": "The Escape"},
                    "id": "tse5863480",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 7, "seasonNumber": 3, "title": "The Siren"},
                    "id": "tse5863486",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 8,
                        "seasonNumber": 3,
                        "title": "The Wellness Center",
                    },
                    "id": "tse5863484",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 9, "seasonNumber": 3, "title": "A Farewell"},
                    "id": "tse5863483",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 10, "seasonNumber": 3, "title": "The Portrait"},
                    "id": "tse5863481",
                },
            ],
            "id": "tss306291",
        },
        {
            "__typename": "Season",
            "content": {"seasonNumber": 4},
            "episodes": [
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 1, "seasonNumber": 4, "title": "Reunited"},
                    "id": "tse6569917",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 2, "seasonNumber": 4, "title": "The Lamp"},
                    "id": "tse6569916",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 3,
                        "seasonNumber": 4,
                        "title": "The Grand Opening",
                    },
                    "id": "tse6569915",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 4, "seasonNumber": 4, "title": "The Night Market"},
                    "id": "tse6638945",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 5, "seasonNumber": 4, "title": "Private School"},
                    "id": "tse6638946",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 6, "seasonNumber": 4, "title": "The Wedding"},
                    "id": "tse6638941",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 7, "seasonNumber": 4, "title": "Pine Barrens"},
                    "id": "tse6638942",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 8, "seasonNumber": 4, "title": "Go Flip Yourself"},
                    "id": "tse6638947",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 9, "seasonNumber": 4, "title": "Freddie"},
                    "id": "tse6638944",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 10, "seasonNumber": 4, "title": "Sunrise, Sunset"},
                    "id": "tse6638943",
                },
            ],
            "id": "tss357215",
        },
        {
            "__typename": "Season",
            "content": {"seasonNumber": 5},
            "episodes": [
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 1, "seasonNumber": 5, "title": "The Mall"},
                    "id": "tse7422284",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 2,
                        "seasonNumber": 5,
                        "title": "A Night Out with the Guys",
                    },
                    "id": "tse7422285",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 3, "seasonNumber": 5, "title": "Pride Parade"},
                    "id": "tse7482502",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 4, "seasonNumber": 5, "title": "The Campaign"},
                    "id": "tse7528347",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 5, "seasonNumber": 5, "title": "Local News"},
                    "id": "tse7528354",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 6, "seasonNumber": 5, "title": "Urgent Care"},
                    "id": "tse7528351",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 7, "seasonNumber": 5, "title": "Hybrid Creatures"},
                    "id": "tse7528350",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 8, "seasonNumber": 5, "title": "The Roast"},
                    "id": "tse7528352",
                },
                {
                    "__typename": "Episode",
                    "content": {
                        "episodeNumber": 9,
                        "seasonNumber": 5,
                        "title": "A Weekend at Morrigan Manor",
                    },
                    "id": "tse7528353",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 10, "seasonNumber": 5, "title": "Exit Interview"},
                    "id": "tse7528349",
                },
            ],
            "id": "tss361882",
        },
        {
            "__typename": "Season",
            "content": {"seasonNumber": 6},
            "episodes": [
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 1, "seasonNumber": 6, "title": "Episode 1"},
                    "id": "tse7528348",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 2, "seasonNumber": 6, "title": "Episode 2"},
                    "id": "tse8544433",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 3, "seasonNumber": 6, "title": "Episode 3"},
                    "id": "tse8544439",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 4, "seasonNumber": 6, "title": "Episode 4"},
                    "id": "tse8544449",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 5, "seasonNumber": 6, "title": "Episode 5"},
                    "id": "tse8544457",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 6, "seasonNumber": 6, "title": "Episode 6"},
                    "id": "tse8544465",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 7, "seasonNumber": 6, "title": "Episode 7"},
                    "id": "tse8544476",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 8, "seasonNumber": 6, "title": "Episode 8"},
                    "id": "tse8544483",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 9, "seasonNumber": 6, "title": "Episode 9"},
                    "id": "tse8544494",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 10, "seasonNumber": 6, "title": "Episode 10"},
                    "id": "tse8544502",
                },
                {
                    "__typename": "Episode",
                    "content": {"episodeNumber": 11, "seasonNumber": 6, "title": "Episode 11"},
                    "id": "tse8544521",
                },
            ],
            "id": "tss361883",
        },
    ],
}

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
        (API_SEARCH_RESPONSE_NO_DATA, []),
    ],
)
def test_parse_search_response(response_json: dict, expected_output: list[MediaEntry]) -> None:
    parsed_entries = parse_search_response(response_json)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=["response_json", "expected_output"],
    argvalues=[
        ({"data": {"node": RESPONSE_NODE_1}}, PARSED_NODE_1),
        ({"data": {"node": RESPONSE_NODE_2}}, PARSED_NODE_2),
        ({"data": {"node": RESPONSE_NODE_3}}, PARSED_NODE_3),
        ({"errors": [], "data": {"node": None}}, None),
    ],
)
def test_parse_details_response(response_json: dict, expected_output: MediaEntry) -> None:
    parsed_entries = parse_details_response(response_json)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=["response_json", "expected_output"],
    argvalues=[
        ({"data": {"node": RESPONSE_NODE_4}}, PARSED_NODE_4),
        ({"errors": [], "data": {"node": None}}, None),
    ],
)
def test_parse_seasons_response(response_json: dict, expected_output: SeasonsEntry) -> None:
    parsed_entries = parse_seasons_response(response_json)
    assert parsed_entries == expected_output


@mark.parametrize(
    argnames=["response_json", "countries", "expected_output"],
    argvalues=[
        (
            {"data": {"node": {"US": RESPONSE_NODE_1["offers"]}}},
            {"US"},
            {"US": PARSED_NODE_1.offers},
        ),
        (
            {"data": {"node": {"US": RESPONSE_NODE_1["offers"], "GB": RESPONSE_NODE_2["offers"]}}},
            {"US", "GB"},
            {"US": PARSED_NODE_1.offers, "GB": PARSED_NODE_2.offers},
        ),
        (
            {"data": {"node": {"US": RESPONSE_NODE_1["offers"], "GB": RESPONSE_NODE_2["offers"]}}},
            {"US"},
            {"US": PARSED_NODE_1.offers},
        ),
        (
            {"data": {"node": {"US": RESPONSE_NODE_1["offers"], "GB": RESPONSE_NODE_2["offers"]}}},
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
def test_parse_offers_for_countries_response(
    response_json: dict, countries: set[str], expected_output: dict[str, list[Offer]]
) -> None:
    parsed_entries = parse_offers_for_countries_response(response_json, countries)
    assert parsed_entries == expected_output
