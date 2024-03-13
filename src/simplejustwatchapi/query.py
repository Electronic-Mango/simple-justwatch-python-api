"""Module responsible for creating GraphQL queries and parsing responses from JustWatch GraphQL API.
Parsed responses are returned as Python NamedTuples for easier access.
Currently only responses from "GetSearchTitles" query are supported.
"""

from typing import NamedTuple

_DETAILS_URL = "https://justwatch.com"
_IMAGES_URL = "https://images.justwatch.com"

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
) {
  popularTitles(
    country: $country
    filter: $searchTitlesFilter
    first: $first
    sortBy: POPULAR
    sortRandomSeed: 0
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

_GRAPHQL_DETAILS_FRAGMENT = """
fragment TitleDetails on MovieOrShow {
  id
  objectId
  objectType
  content(country: $country, language: $language) {
    title
    fullPath
    originalReleaseYear
    originalReleaseDate
    runtime
    shortDescription
    genres {
      shortName
      __typename
    }
    externalIds {
      imdbId
      __typename
    }
    posterUrl(profile: $profile, format: $formatPoster)
    backdrops(profile: $backdropProfile, format: $formatPoster) {
      backdropUrl
      __typename
    }
    __typename
  }
  offers(country: $country, platform: WEB, filter: $filter) {
    ...TitleOffer
  }
  __typename
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


class OfferPackage(NamedTuple):
    """Parsed single offer package from JustWatch GraphQL API for single entry."""

    id: str
    package_id: int
    name: str
    technical_name: str
    icon: str


class Offer(NamedTuple):
    """Parsed single offer from JustWatch GraphQL API for single entry."""

    id: str
    monetization_type: str
    presentation_type: str
    price_string: str | None
    price_value: float | None
    price_currency: str
    last_change_retail_price_value: float | None
    type: str
    package: OfferPackage
    url: str
    element_count: int
    available_to: str | None
    deeplink_roku: str | None
    subtitle_languages: list[str]
    video_technology: list[str]
    audio_technology: list[str]
    audio_languages: list[str]


class MediaEntry(NamedTuple):
    """Parsed response from JustWatch GraphQL API for "GetSearchTitles" query for single entry."""

    entry_id: str
    object_id: int
    object_type: str
    title: str
    url: str
    release_year: int
    release_date: str
    runtime_minutes: int
    short_description: str
    genres: list[str]
    imdb_id: str | None
    poster: str | None
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
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": _GRAPHQL_SEARCH_QUERY + _GRAPHQL_DETAILS_FRAGMENT + _GRAPHQL_OFFER_FRAGMENT,
    }


def parse_search_response(json: dict) -> list[MediaEntry]:
    """Parse response from search query from JustWatch GraphQL API.
    Parses response for "GetSearchTitles" query.
    If API didn't return any data, then an empty list is returned.

    Args:
        json: JSON returned by JustWatch GraphQL API

    Returns:
        Parsed received JSON as a list of MediaEntry NamedTuples
    """
    nodes = json["data"]["popularTitles"]["edges"]
    entries = [_parse_entry(node["node"]) for node in nodes]
    return entries


def prepare_details_request(node_id: str, country: str, language: str, best_only: bool) -> dict:
    """Prepare a details request for specified node ID to JustWatch GraphQL API.
    Creates a "GetTitleNode" GraphQL query.
    Country code should be two uppercase letters, however it will be auto-converted to uppercase.

    Args:
        node_id: node ID of entry to get details for
        country: country to search for offers
        language: language of responses
        best_only: return only best offers if True, return all offers if False

    Returns:
        JSON/dict with GraphQL POST body
    """
    assert len(country) == 2, f"Invalid country code: {country}, code must be 2 characters long"
    return {
        "operationName": "GetTitleNode",
        "variables": {
            "nodeId": node_id,
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": _GRAPHQL_DETAILS_QUERY + _GRAPHQL_DETAILS_FRAGMENT + _GRAPHQL_OFFER_FRAGMENT,
    }


def parse_details_response(json: any) -> MediaEntry | None:
    """Parse response from details query from JustWatch GraphQL API.
    Parses response for "GetTitleNode" query.
    If API responded with an internal error (mostly due to not found node ID),
    then "None" will be returned instead.

    Args:
        json: JSON returned by JustWatch GraphQL API

    Returns:
        Parsed received JSON as a MediaEntry NamedTuple,
        or None in case data for a given node ID was not found
    """
    return _parse_entry(json["data"]["node"]) if "errors" not in json else None


def _parse_entry(json: any) -> MediaEntry:
    entry_id = json.get("id")
    object_id = json.get("objectId")
    object_type = json.get("objectType")
    content = json["content"]
    title = content.get("title")
    url = _DETAILS_URL + content.get("fullPath")
    year = content.get("originalReleaseYear")
    date = content.get("originalReleaseDate")
    runtime_minutes = content.get("runtime")
    short_description = content.get("shortDescription")
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
        runtime_minutes,
        short_description,
        genres,
        imdb_id,
        poster,
        backdrops,
        offers,
    )


def _parse_offer(json: any) -> Offer:
    id = json.get("id")
    monetization_type = json.get("monetizationType")
    presentation_type = json.get("presentationType")
    price_string = json.get("retailPrice")
    price_value = json.get("retailPriceValue")
    price_currency = json.get("currency")
    last_change_retail_price_value = json.get("lastChangeRetailPriceValue")
    type = json.get("type")
    package = _parse_package(json["package"])
    url = json.get("standardWebURL")
    element_count = json.get("elementCount", 0)
    available_to = json.get("availableTo")
    deeplink_roku = json.get("deeplinkRoku")
    subtitle_languages = json.get("subtitleLanguages")
    video_technology = json.get("videoTechnology")
    audio_technology = json.get("audioTechnology")
    audio_languages = json.get("audioLanguages")
    return Offer(
        id,
        monetization_type,
        presentation_type,
        price_string,
        price_value,
        price_currency,
        last_change_retail_price_value,
        type,
        package,
        url,
        element_count,
        available_to,
        deeplink_roku,
        subtitle_languages,
        video_technology,
        audio_technology,
        audio_languages,
    )


def _parse_package(json: any) -> OfferPackage:
    id = json.get("id")
    package_id = json.get("packageId")
    name = json.get("clearName")
    technical_name = json.get("technicalName")
    icon = _IMAGES_URL + json.get("icon")
    return OfferPackage(id, package_id, name, technical_name, icon)
