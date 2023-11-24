from typing import NamedTuple

_DETAILS_URL = "https://justwatch.com"
_IMAGES_URL = "https://images.justwatch.com"


class Offer(NamedTuple):
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
    entry_id: str
    object_id: int
    object_type: str
    title: str
    url: str
    release_year: int
    release_date: str
    genres: list[str]
    imdb_id: str
    poster: str
    backdrops: list[str]
    offers: list[Offer]


def parse_search_response(json: dict) -> list[MediaEntry]:
    """Parse response from search query from JustWatch GraphQL API.

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
    poster = _IMAGES_URL + content.get("posterUrl")
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
