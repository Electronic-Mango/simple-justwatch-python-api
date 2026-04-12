from pytest import mark

from simplejustwatchapi.graphql import (
    GRAPHQL_DETAILS_QUERY,
    GRAPHQL_EPISODES_QUERY,
    GRAPHQL_POPULAR_QUERY,
    GRAPHQL_PROVIDERS_QUERY,
    GRAPHQL_SEARCH_QUERY,
    GRAPHQL_SEASONS_QUERY,
    graphql_offers_for_countries_query,
)

PACKAGE_ELEMENTS = [
    "...PackageDetails",
    "fragment PackageDetails on Package",
]

COMMON_ELEMENTS = [
    "title",
    "id",
    "objectId",
    "objectType",
    "content(country: $country, language: $language)",
    "offers(country: $country, platform: WEB, filter: $filter)",
    "...TitleDetails",
    "fragment TitleDetails",
    "...ContentDetails",
    "fragment ContentDetails on MovieOrShowOrSeasonOrEpisodeContent",
    "...FullContentDetails",
    "fragment FullContentDetails on MovieOrShowOrSeasonContent",
    "...TitleOffer",
    "fragment TitleOffer on Offer",
    *PACKAGE_ELEMENTS,
]


def assert_query_contains_elements(query, elements):
    assert all(element in query for element in elements)


@mark.parametrize(
    argnames=("query", "expected_elements"),
    argvalues=[
        (
            GRAPHQL_DETAILS_QUERY,
            ["query GetTitleNode", "node(id: $nodeId)", *COMMON_ELEMENTS],
        ),
        (
            GRAPHQL_EPISODES_QUERY,
            [
                "query GetTitleNode",
                "... on Season",
                "episodes(sortDirection: ASC)",
                *COMMON_ELEMENTS,
            ],
        ),
        (
            GRAPHQL_POPULAR_QUERY,
            [
                "query GetPopularTitles",
                "$popularTitlesFilter: TitleFilter",
                "popularTitles(",
                *COMMON_ELEMENTS,
            ],
        ),
        (
            GRAPHQL_PROVIDERS_QUERY,
            [
                "query GetProviders",
                "$country: Country!",
                "packages(",
                *PACKAGE_ELEMENTS,
            ],
        ),
        (
            GRAPHQL_SEARCH_QUERY,
            [
                "query GetSearchTitles",
                "$searchTitlesFilter: TitleFilter!",
                "popularTitles(",
                *COMMON_ELEMENTS,
            ],
        ),
        (
            GRAPHQL_SEASONS_QUERY,
            [
                "query GetTitleNode",
                "... on Show",
                "seasons(sortDirection: ASC)",
                *COMMON_ELEMENTS,
            ],
        ),
    ],
)
def test_graphql_simple_query(query, expected_elements):
    assert_query_contains_elements(query, expected_elements)


@mark.parametrize("country_codes", [{"gb", "Us", "fR", "CA"}, {"us"}, set()])
def test_graphql_offers_for_countries_query(country_codes):
    query = graphql_offers_for_countries_query(country_codes)
    expected_elements = ["query GetTitleOffers", "node(id: $nodeId)", *PACKAGE_ELEMENTS]
    country_code_offers = [
        f"{country_code.upper()}: offers(country: {country_code.upper()}, "
        "platform: WEB, filter: $filter)"
        for country_code in country_codes
    ]
    expected_elements.extend(country_code_offers)
    assert_query_contains_elements(query, expected_elements)
    assert query.count("...TitleOffer") == len(country_codes)
