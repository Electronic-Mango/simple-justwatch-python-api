"""Module responsible for creating GraphQL queries and parsing responses from JustWatch GraphQL API.
Parsed responses are returned as Python NamedTuples for easier access.
Currently only responses from "GetSearchTitles" query are supported.
"""

from typing import NamedTuple

_DETAILS_URL = "https://justwatch.com"
_IMAGES_URL = "https://images.justwatch.com"


_GRAPHQL_SEARCH_QUERY = """
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


class Offer(NamedTuple):
    """Parsed single offer from JustWatch GraphQL API for single entry.
    Doesn't match fully received response, some fields are simplified.
    """

    monetization_type: str
    presentation_type: str
    url: str
    price_string: str | None
    price_value: float | None
    price_currency: str
    name: str
    technical_name: str
    icon: str


class MediaEntry(NamedTuple):
    """Parsed response from JustWatch GraphQL API for "GetSearchTitles" query for single entry.
    Doesn't match fully received response, some fields are simplified.
    """

    entry_id: str
    object_id: int
    object_type: str
    title: str
    url: str
    release_year: int
    release_date: str
    genres: list[str]
    imdb_id: str | None
    poster: str
    backdrops: list[str]
    offers: list[Offer]


def prepare_search_request(
    title: str, country: str, language: str, count: int, best_only: bool
) -> dict:
    """Prepare search request for JustWatch GraphQL API.
    Creates a "GetSearchTitles" GraphQL query.
    Country code should be two uppercase letters, however it will be auto-converted to uppercase.

    Args:
        title: title to search
        country: country to search for offers
        language: language of responses
        count: how many responses should be returned
        best_only: return only best offers if True, return all offers if False

    Returns:
        JSON/dict with GraphQL POST body
    """
    assert len(country) == 2, f"Invalid country code: {country}, code must be 2 characters long"
    return {
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
        "query": _GRAPHQL_SEARCH_QUERY,
    }


def parse_search_response(json: dict) -> list[MediaEntry]:
    """Parse response from search query from JustWatch GraphQL API.
    Parses response for "GetSearchTitles" query.

    Args:
        json: JSON returned by JustWatch GraphQL API

    Returns:
        Parsed received JSON as a MediaEntry NamedTuple
    """
    nodes = json["data"]["popularTitles"]["edges"]
    entries = [_parse_entry(node["node"]) for node in nodes]
    return entries


def _parse_entry(json: any) -> MediaEntry:
    entry_id = json.get("id")
    object_id = json.get("objectId")
    object_type = json.get("objectType")
    content = json["content"]
    title = content.get("title")
    url = _DETAILS_URL + content.get("fullPath")
    year = content.get("originalReleaseYear")
    date = content.get("originalReleaseDate")
    genres = [node.get("shortName") for node in content.get("genres", []) if node]
    external_ids = content.get("externalIds")
    imdb_id = external_ids.get("imdbId") if external_ids else None
    poster_url_field = content.get("posterUrl")
    poster = _IMAGES_URL + poster_url_field if poster_url_field else None
    backdrops = [_IMAGES_URL + bd.get("backdropUrl") for bd in content.get("backdrops", []) if bd]
    offers = [_parse_offer(offer) for offer in json.get("offers", []) if offer]
    return MediaEntry(
        entry_id,
        object_id,
        object_type,
        title,
        url,
        year,
        date,
        genres,
        imdb_id,
        poster,
        backdrops,
        offers,
    )


def _parse_offer(json: any) -> Offer:
    monetization_type = json.get("monetizationType")
    presentation_type = json.get("presentationType")
    url = json.get("standardWebURL")
    price_string = json.get("retailPrice")
    price_value = json.get("retailPriceValue")
    price_currency = json.get("currency")
    package = json["package"]
    name = package.get("clearName")
    technical_name = package.get("technicalName")
    icon = _IMAGES_URL + package.get("icon")
    return Offer(
        monetization_type,
        presentation_type,
        url,
        price_string,
        price_value,
        price_currency,
        name,
        technical_name,
        icon,
    )
