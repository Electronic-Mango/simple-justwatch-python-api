GRAPHQL_SEARCH_QUERY = """
query GetSearchTitles(
  $searchTitlesFilter: TitleFilter!,
  $country: Country!,
  $language: Language!,
  $first: Int!,
  $format: ImageFormat,
  $profile: PosterProfile,
  $backdropProfile: BackdropProfile,
  $filter: OfferFilter!,
) {
  popularTitles(
    country: $country
    filter: $searchTitlesFilter
    first: $first
    sortBy: POPULAR
    sortRandomSeed: 0
  ) {
    edges {
      ...SearchTitleGraphql
      __typename
    }
    __typename
  }
}

fragment SearchTitleGraphql on PopularTitlesEdge {
  node {
    id
    objectId
    objectType
    content(country: $country, language: $language) {
      title
      fullPath
      originalReleaseYear
      originalReleaseDate
      genres {
        shortName
        __typename
      }
      externalIds {
        imdbId
        __typename
      }
      posterUrl(profile: $profile, format: $format)
      backdrops(profile: $backdropProfile, format: $format) {
        backdropUrl
        __typename
      }
      __typename
    }
    offers(country: $country, platform: WEB, filter: $filter) {
      monetizationType
      presentationType
      standardWebURL
      retailPrice(language: $language)
      retailPriceValue
      currency
      package {
        id
        packageId
        clearName
        technicalName
        icon(profile: S100)
        __typename
      }
      id
      __typename
    }
    __typename
  }
  __typename
}
"""


def prepare_search_request(title: str, county: str, lang: str, count: int, best_only: bool) -> dict:
    """Prepare search request for JustWatch GraphQL API.

    Args:
        title: title to search
        county: country to search for offers
        lang: language of responses
        count: how many responses should be returned
        best_only: return only best offers if True, return all offers if False

    Returns:
        JSON/dict with GraphQL POST body
    """
    return {
        "operationName": "GetSearchTitles",
        "variables": {
            "first": count,
            "searchTitlesFilter": {"searchQuery": title},
            "language": lang,
            "country": county,
            "format": "JPG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": GRAPHQL_SEARCH_QUERY,
    }
