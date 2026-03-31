from pytest import mark

from simplejustwatchapi.graphql import (
    graphql_details_query,
    graphql_episodes_query,
    graphql_offers_for_countries_query,
    graphql_search_query,
    graphql_seasons_query,
)

GRAPHQL_SEARCH_QUERY = """
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

GRAPHQL_DETAILS_QUERY = """
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

GRAPHQL_SEASONS_QUERY = """
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

GRAPHQL_EPISODES_QUERY = """
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

GRAPHQL_OFFERS_BY_COUNTRY_QUERY = """
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

GRAPHQL_DETAILS_FRAGMENT = """
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

GRAPHQL_OFFER_FRAGMENT = """
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

GRAPHQL_COUNTRY_OFFERS_ENTRY = """
      {country_code}: offers(country: {country_code}, platform: WEB, filter: $filter) {{
        ...TitleOffer
        __typename
      }}
"""


def test_graphql_search_query():
    expected_query = GRAPHQL_SEARCH_QUERY + GRAPHQL_DETAILS_FRAGMENT + GRAPHQL_OFFER_FRAGMENT
    query = graphql_search_query()
    assert expected_query == query


def test_graphql_details_query():
    expected_query = GRAPHQL_DETAILS_QUERY + GRAPHQL_DETAILS_FRAGMENT + GRAPHQL_OFFER_FRAGMENT
    query = graphql_details_query()
    assert expected_query == query


def test_graphql_seasons_query():
    expected_query = GRAPHQL_SEASONS_QUERY + GRAPHQL_DETAILS_FRAGMENT + GRAPHQL_OFFER_FRAGMENT
    query = graphql_seasons_query()
    assert expected_query == query


def test_graphql_episodes_query():
    expected_query = GRAPHQL_EPISODES_QUERY + GRAPHQL_DETAILS_FRAGMENT + GRAPHQL_OFFER_FRAGMENT
    query = graphql_episodes_query()
    assert expected_query == query


@mark.parametrize("country_codes", [{"gb", "Us", "fR", "CA"}, {"us"}, set()])
def test_graphql_offers_for_countries_query(country_codes):
    offer_requests = [
        GRAPHQL_COUNTRY_OFFERS_ENTRY.format(country_code=country_code.upper())
        for country_code in country_codes
    ]
    main_body = GRAPHQL_OFFERS_BY_COUNTRY_QUERY.format(country_entries="\n".join(offer_requests))
    expected_query = main_body + GRAPHQL_OFFER_FRAGMENT
    query = graphql_offers_for_countries_query(country_codes)
    assert expected_query == query
