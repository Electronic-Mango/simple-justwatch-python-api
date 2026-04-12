"""
Module responsible for preparing full GraphQL queries.

Queries are usually prepared as main query + needed fragments.
Specific details are stored as separate GraphQL fragments / Python strings for easier
reuse and maintainability.
"""

_GRAPHQL_SEARCH_QUERY = """
query GetSearchTitles(
    $searchTitlesFilter: TitleFilter!,
    $country: Country!,
    $language: Language!,
    $first: Int!,
    $formatPoster: ImageFormat,
    $formatOfferIcon: ImageFormat,
    $profile: PosterProfile,
    $backdropProfile: BackdropProfile,
    $filter: OfferFilter!,
    $offset: Int = 0,
) {
    popularTitles(
        country: $country
        filter: $searchTitlesFilter
        first: $first
        sortBy: POPULAR
        sortRandomSeed: 0
        offset: $offset
    ) {
        edges {
            node {
                ...TitleDetails
                __typename
            }
            __typename
        }
        __typename
    }
}
"""

_GRAPHQL_POPULAR_QUERY = """
query GetPopularTitles(
    $popularTitlesFilter: TitleFilter
    $country: Country!
    $language: Language!
    $first: Int! = 70
    $formatPoster: ImageFormat,
    $formatOfferIcon: ImageFormat,
    $profile: PosterProfile
    $backdropProfile: BackdropProfile,
    $filter: OfferFilter!,
    $offset: Int = 0
) {
    popularTitles(
        country: $country
        filter: $popularTitlesFilter
        first: $first
        sortBy: POPULAR
        sortRandomSeed: 0
        offset: $offset
    ) {
        __typename
        edges {
            node {
                ...TitleDetails
                __typename
            }
            __typename
        }
    }
}
"""

_GRAPHQL_DETAILS_QUERY = """
query GetTitleNode(
    $nodeId: ID!,
    $language: Language!,
    $country: Country!,
    $formatPoster: ImageFormat,
    $formatOfferIcon: ImageFormat,
    $profile: PosterProfile,
    $backdropProfile: BackdropProfile,
    $filter: OfferFilter!,
) {
    node(id: $nodeId) {
        ...TitleDetails
        __typename
    }
    __typename
}
"""

_GRAPHQL_SEASONS_QUERY = """
query GetTitleNode(
    $nodeId: ID!,
    $language: Language!,
    $country: Country!,
    $formatPoster: ImageFormat,
    $formatOfferIcon: ImageFormat,
    $profile: PosterProfile,
    $backdropProfile: BackdropProfile,
    $filter: OfferFilter!,
) {
    node(id: $nodeId) {
        ... on Show {
            seasons(sortDirection: ASC) {
                ...TitleDetails
            }
        }
        __typename
    }
    __typename
}
"""

_GRAPHQL_EPISODES_QUERY = """
query GetTitleNode(
    $nodeId: ID!,
    $language: Language!,
    $country: Country!,
    $formatPoster: ImageFormat,
    $formatOfferIcon: ImageFormat,
    $profile: PosterProfile,
    $backdropProfile: BackdropProfile,
    $filter: OfferFilter!,
) {
    node(id: $nodeId) {
        ... on Season {
            episodes(sortDirection: ASC) {
                ...TitleDetails
            }
        }
        __typename
    }
    __typename
}
"""

_GRAPHQL_PROVIDERS_QUERY = """
query GetProviders(
    $country: Country!,
    $formatOfferIcon: ImageFormat
) {
    packages(
        country: $country
        platform: WEB
        includeAddons: true
    ) {
        ...PackageDetails
    }
    __typename
}
"""

_GRAPHQL_OFFERS_BY_COUNTRY_QUERY = """
query GetTitleOffers(
    $nodeId: ID!,
    $language: Language!,
    $formatOfferIcon: ImageFormat,
    $filter: OfferFilter!,
) {{
    node(id: $nodeId) {{
        ... on MovieOrShowOrSeasonOrEpisode {{
            {country_entries}
            __typename
        }}
        __typename
    }}
    __typename
}}
"""

_GRAPHQL_DETAILS_FRAGMENT = """
fragment TitleDetails on MovieOrShowOrSeasonOrEpisode {
    id
    objectId
    objectType
    content(country: $country, language: $language) {
        ...ContentDetails
        __typename
    }
    ...StreamingChartInfoFragment
    ... on Show {
        totalSeasonCount
    }
    ... on Season {
        totalEpisodeCount
    }
    offers(country: $country, platform: WEB, filter: $filter) {
        ...TitleOffer
    }
    __typename
}

fragment StreamingChartInfoFragment on MovieOrShowOrSeason {
    streamingCharts(country: $country) {
        edges {
            streamingChartInfo {
                rank
                trend
                trendDifference
                daysInTop3
                daysInTop10
                daysInTop100
                daysInTop1000
                topRank
                updatedAt
                __typename
            }
            __typename
        }
        __typename
    }
}

fragment ContentDetails on MovieOrShowOrSeasonOrEpisodeContent {
    title
    originalReleaseYear
    originalReleaseDate
    runtime
    shortDescription
    ...FullContentDetails
    ... on MovieOrShowContent {
        ageCertification
    }
    ... on SeasonContent {
        seasonNumber
    }
    ... on EpisodeContent {
        seasonNumber
        episodeNumber
    }
}

fragment FullContentDetails on MovieOrShowOrSeasonContent {
    fullPath
    genres {
        shortName
        __typename
    }
    externalIds {
        imdbId
        tmdbId
        __typename
    }
    posterUrl(profile: $profile, format: $formatPoster)
    backdrops(profile: $backdropProfile, format: $formatPoster) {
        backdropUrl
        __typename
    }
    scoring {
        imdbScore
        imdbVotes
        tmdbPopularity
        tmdbScore
        tomatoMeter
        certifiedFresh
        jwRating
        __typename
    }
    interactions {
        likelistAdditions
        dislikelistAdditions
        __typename
    }
}
"""

_GRAPHQL_OFFER_FRAGMENT = """
fragment TitleOffer on Offer {
    id
    monetizationType
    presentationType
    retailPrice(language: $language)
    retailPriceValue
    currency
    lastChangeRetailPriceValue
    type
    package {
        ...PackageDetails
    }
    standardWebURL
    elementCount
    availableTo
    deeplinkRoku: deeplinkURL(platform: ROKU_OS)
    subtitleLanguages
    videoTechnology
    audioTechnology
    audioLanguages
    __typename
}
"""

_GRAPHQL_PACKAGE_FRAGMENT = """
fragment PackageDetails on Package {
    id
    packageId
    clearName
    technicalName
    shortName
    slug
    monetizationTypes
    icon(profile: S100, format: $formatOfferIcon)
    __typename
}
"""

_GRAPHQL_COUNTRY_OFFERS_ENTRY = """
{country_code}: offers(country: {country_code}, platform: WEB, filter: $filter) {{
    ...TitleOffer
    __typename
}}
"""

GRAPHQL_SEARCH_QUERY = (
    _GRAPHQL_SEARCH_QUERY
    + _GRAPHQL_DETAILS_FRAGMENT
    + _GRAPHQL_OFFER_FRAGMENT
    + _GRAPHQL_PACKAGE_FRAGMENT
)

GRAPHQL_POPULAR_QUERY = (
    _GRAPHQL_POPULAR_QUERY
    + _GRAPHQL_DETAILS_FRAGMENT
    + _GRAPHQL_OFFER_FRAGMENT
    + _GRAPHQL_PACKAGE_FRAGMENT
)

GRAPHQL_PROVIDERS_QUERY = _GRAPHQL_PROVIDERS_QUERY + _GRAPHQL_PACKAGE_FRAGMENT

GRAPHQL_DETAILS_QUERY = (
    _GRAPHQL_DETAILS_QUERY
    + _GRAPHQL_DETAILS_FRAGMENT
    + _GRAPHQL_OFFER_FRAGMENT
    + _GRAPHQL_PACKAGE_FRAGMENT
)

GRAPHQL_SEASONS_QUERY = (
    _GRAPHQL_SEASONS_QUERY
    + _GRAPHQL_DETAILS_FRAGMENT
    + _GRAPHQL_OFFER_FRAGMENT
    + _GRAPHQL_PACKAGE_FRAGMENT
)

GRAPHQL_EPISODES_QUERY = (
    _GRAPHQL_EPISODES_QUERY
    + _GRAPHQL_DETAILS_FRAGMENT
    + _GRAPHQL_OFFER_FRAGMENT
    + _GRAPHQL_PACKAGE_FRAGMENT
)


def graphql_offers_for_countries_query(countries: set[str]) -> str:
    """
    Prepare GraphQL query with a list of offers from specified countries.

    The full query is `GetTitleOffers` query with a list of offers per country.
    No additional information is returned, only offers.
    Can be used for all entry types - movies, shows, seasons, episodes.

    The input is a set of 2-letter country codes. This function assumes that codes are
    valid length and the set is not empty; it performs no verification on its own.

    Args:
        countries (set[str]): 2-letter country codes.

    Returns:
        (str): GraphQL `GetTitleOffers` query with available offers per country code.

    """
    offer_requests = [
        _GRAPHQL_COUNTRY_OFFERS_ENTRY.format(country_code=country_code.upper())
        for country_code in countries
    ]
    main_query = _GRAPHQL_OFFERS_BY_COUNTRY_QUERY.format(
        country_entries="\n".join(offer_requests)
    )
    return main_query + _GRAPHQL_OFFER_FRAGMENT + _GRAPHQL_PACKAGE_FRAGMENT
