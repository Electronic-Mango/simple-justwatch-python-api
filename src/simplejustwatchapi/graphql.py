"""
Module responsible for preparing full GraphQL queries.

Queries are usually prepared as main query + details fragment + offers fragment.

In the long term these queries should be moved to dedicated GraphQL resource files
to allow for formatting and syntax checking. However, the functions used for constructing
full queries shouldn't change.
"""

# TODO: Convert these strings into resources, e.g.:
#       https://docs.python.org/3/library/importlib.resources.html

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
    ...on Show {
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
    ...on Season {
      episodes(sortDirection: ASC) {
        ...TitleDetails
      }
    }
    __typename
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
  ...on Show {
    totalSeasonCount
  }
  ...on Season {
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
  ...on MovieOrShowContent {
    ageCertification
  }
  ...on SeasonContent {
    seasonNumber
  }
  ...on EpisodeContent {
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
    id
    packageId
    clearName
    technicalName
    icon(profile: S100, format: $formatOfferIcon)
    __typename
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

_GRAPHQL_COUNTRY_OFFERS_ENTRY = """
      {country_code}: offers(country: {country_code}, platform: WEB, filter: $filter) {{
        ...TitleOffer
        __typename
      }}
"""


def graphql_search_query() -> str:
    """
    Prepare GraphQL query used for searching for entries.

    The query is GetSearchTitles query + details fragment + offers fragment.

    Returns:
        str: Full GraphQL "search" query.

    """
    return _GRAPHQL_SEARCH_QUERY + _GRAPHQL_DETAILS_FRAGMENT + _GRAPHQL_OFFER_FRAGMENT


def graphql_details_query() -> str:
    """
    Prepare GraphQL query used for getting details regarding a single entry.

    The full query is GetTitleNode query + details fragment + offers fragment.
    It is meant for movies and shows, but can be used for seasons and episodes as well,
    it just won't return full season/episodes list.

    Returns:
        str: Full GraphQL "get details" query.

    """
    return _GRAPHQL_DETAILS_QUERY + _GRAPHQL_DETAILS_FRAGMENT + _GRAPHQL_OFFER_FRAGMENT


def graphql_seasons_query() -> str:
    """
    Prepare GraphQL query used for getting a list of seasons for a single show.

    The full query is GetTitleNode query (with seasons list) + details fragment + offers fragment.
    It will only return data for shows with a list of all available seasons, ascending.
    Details query itself matches :func:`graphql_details_query`, its conditions will return all
    relevant data for seasons.

    Returns:
        str: Full GraphQL "get seasons" query.

    """
    return _GRAPHQL_SEASONS_QUERY + _GRAPHQL_DETAILS_FRAGMENT + _GRAPHQL_OFFER_FRAGMENT


def graphql_episodes_query() -> str:
    """
    Prepare GraphQL query used for getting a list of episodes for a single show season.

    The full query is GetTitleNode query (with episodes list) + details fragment + offers fragment.
    It will only return data for show seasons with a list of all available episodes, ascending.
    Details query itself matches :func:`graphql_details_query`, its conditions will return all
    relevant data for episodes.

    Returns:
        str: Full GraphQL "get episodes" query.

    """
    return _GRAPHQL_EPISODES_QUERY + _GRAPHQL_DETAILS_FRAGMENT + _GRAPHQL_OFFER_FRAGMENT


def graphql_offers_for_countries_query(countries: set[str]) -> str:
    """
    Prepare GraphQL query with a list of offers from specified countries.

    The full query is GetTitleOffers query with a list of offers per country.
    No additional information is returned, only offers.
    Can be used for all entry types - movies, shows, seasons, episodes.

    The input is a set of 2-letter country codes. This function assumes that codes are valid length,
    the set is not empty; it performs no additional verification.

    Args:
        countries (set[str]): 2-letter country codes.

    Returns:
        str: Full GraphQL "get offers per country" query.

    """
    offer_requests = [
        _GRAPHQL_COUNTRY_OFFERS_ENTRY.format(country_code=country_code.upper())
        for country_code in countries
    ]
    main_query = _GRAPHQL_OFFERS_BY_COUNTRY_QUERY.format(country_entries="\n".join(offer_requests))
    return main_query + _GRAPHQL_OFFER_FRAGMENT
