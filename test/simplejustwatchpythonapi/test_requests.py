from pytest import mark, raises

from simplejustwatchpythonapi.requests import prepare_search_request

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


@mark.parametrize(
    argnames=["title", "country", "language", "count", "best_only"],
    argvalues=[
        ("TITLE 1", "US", "language 1", 5, True),
        ("TITLE 2", "gb", "language 2", 10, False),
    ]
)
def test_prepare_search_request(title: str, country: str, language: str, count: int, best_only: bool) -> None:
    expected_request = {
        "operationName": "GetSearchTitles",
        "variables": {
            "first": count,
            "searchTitlesFilter": {"searchQuery": title},
            "language": language,
            "country": country.upper(),
            "format": "JPG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": GRAPHQL_SEARCH_QUERY,
    }
    request = prepare_search_request(title, country, language, count, best_only)
    assert expected_request == request


@mark.parametrize(
    argnames=["invalid_code"],
    argvalues=[
        ("United Stated of America",),  # too long
        ("usa",),  # too long
        ("u",),  # too short
    ]
)
def test_prepare_search_request_asserts_on_invalid_country_code(invalid_code: str) -> None:
    expected_error_message = f"Invalid country code: {invalid_code}, code must be 2 characters long"
    with raises(AssertionError) as error:
        prepare_search_request("", invalid_code, "", 1, True)
        assert str(error.value) == expected_error_message
