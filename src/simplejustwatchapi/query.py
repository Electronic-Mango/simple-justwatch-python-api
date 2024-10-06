"""Module responsible for creating GraphQL queries and parsing responses from JustWatch GraphQL API.
Parsed responses are returned as Python NamedTuples for easier access."""

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

_GRAPHQL_OFFERS_BY_COUNTRY_QUERY = """
query GetTitleOffers(
  $nodeId: ID!,
  $language: Language!,
  $formatOfferIcon: ImageFormat,
  $filter: OfferFilter!,
) {{
  node(id: $nodeId) {{
    ... on MovieOrShow {{
      {country_entries}
      __typename
    }}
    __typename
  }}
  __typename
}}
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
      tmdbId
      __typename
    }
    posterUrl(profile: $profile, format: $formatPoster)
    backdrops(profile: $backdropProfile, format: $formatPoster) {
      backdropUrl
      __typename
    }
    ageCertification
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
    __typename
  }
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

_GRAPHQL_COUNTRY_OFFERS_ENTRY = """
      {country_code}: offers(country: {country_code}, platform: WEB, filter: $filter) {{
        ...TitleOffer
        __typename
      }}
"""


class OfferPackage(NamedTuple):
    """Parsed single offer package from JustWatch GraphQL API for single entry.
    Contains information about platform on which given offer is available."""

    id: str
    """ID, defines whole platform on which this offer is available, not a single offer."""

    package_id: int
    """Package ID, defines whole platform on which this offer is available, not a single offer."""

    name: str
    """Name of the platform in format suited to display for users."""

    technical_name: str
    """Technical name of the platform, usually all lowercase with no whitespaces."""

    icon: str
    """Platform icon URL."""


class Offer(NamedTuple):
    """Parsed single offer from JustWatch GraphQL API for single entry.
    One platform can have multiple offers for one entry available, e.g. renting, buying, etc."""

    id: str
    """Offer ID."""

    monetization_type: str
    """Type of monetization of this offer, e.g. ``FLATRATE`` (streaming), ``RENT``, ``BUY``."""

    presentation_type: str
    """Quality of media in this offer, e.g. ``HD``, ``SD``, ``4K``."""

    price_string: str | None
    """Current price as a string with currency, suitable for displaying to users.
    Format can change based on used ``language`` argument."""

    price_value: float | None
    """Current price as a numeric value."""

    price_currency: str
    """Represents only currency, without price, or value."""

    last_change_retail_price_value: float | None
    """Previous available price if change in price was recorded."""

    type: str
    """Type of offer."""

    package: OfferPackage
    """Information about platform on which this offer is available."""

    url: str
    """URL to this offer."""

    element_count: int | None
    """Element count, usually 0."""

    available_to: str | None
    """Date until which this offer will be available."""

    deeplink_roku: str | None
    """Deeplink to this offer in Roku."""

    subtitle_languages: list[str]
    """List of 2-letter language codes of available subtitles, e.g. ``["en", "pt", "de"]``."""

    video_technology: list[str]
    """List of known video technologies available in this offer, e.g. ``DOLBY_VISION``."""

    audio_technology: list[str]
    """List of known audio technologies available in this offer, e.g. ``DOLBY_ATMOS``."""

    audio_languages: list[str]
    """List of 2-letter language codes of available audio tracks, e.g. ``["en", "pt", "de"]``."""


class Scoring(NamedTuple):
    """Parsed data related to user scoring for a single entry."""

    imdb_score: float | None
    """IMDB score."""

    imdb_votes: int | None
    """Number of votes on IMDB."""

    tmdb_popularity: float | None
    """TMDB popularity score."""

    tmdb_score: float | None
    """TMDB score."""

    tomatometer: int | None
    """Tomatometer score on Rotten Tomatoes."""

    certified_fresh: bool | None
    """Flag whether entry has "Certified Fresh" seal on Rotten Tomatoes."""

    jw_rating: float | None
    """JustWatch rating."""


class Interactions(NamedTuple):
    """Parsed data regarding number of likes and dislikes on JustWatch for a single entry."""

    likes: int | None
    """Number of likes on JustWatch."""

    dislikes: int | None
    """Number of dislikes on JustWatch."""


class StreamingCharts(NamedTuple):
    """Parsed data related to JustWatch rank for a single entry."""

    rank: int
    """Rank on JustWatch."""

    trend: str
    """Trend in ranking on JustWatch, "UP", "DOWN", "STABLE"."""

    trend_difference: int
    """Difference in rank; related to trend."""

    top_rank: int
    """Top rank ever reached."""

    days_in_top_3: int
    """Number of days in top 3 ranks."""

    days_in_top_10: int
    """Number of days in top 10 ranks."""

    days_in_top_100: int
    """Number of days in top 100 ranks."""

    days_in_top_1000: int
    """Number of days in top 1000 ranks."""

    updated: str
    """Date when rank data was last updated as a string, e.g.: "2024-10-06T09:20:36.397Z"."""


class MediaEntry(NamedTuple):
    """Parsed response from JustWatch GraphQL API for "GetSearchTitles" query for single entry."""

    entry_id: str
    """Entry ID, contains type code and numeric ID."""

    object_id: int
    """Object ID, the numeric part of full entry ID."""

    object_type: str
    """Type of entry, e.g. ``MOVIE``, ``SHOW``."""

    title: str
    """Full title."""

    url: str
    """URL to JustWatch with details for this entry."""

    release_year: int
    """Release year as a number."""

    release_date: str
    """Full release date as a string, e.g. ``2013-12-16``."""

    runtime_minutes: int
    """Runtime in minutes."""

    short_description: str
    """Short description of this entry."""

    genres: list[str]
    """List of genre codes for this entry, e.g. ``["rly"]``, ``["cmy", "drm", "rma"]``."""

    imdb_id: str | None
    """ID of this entry in IMDB."""

    tmdb_id: str | None
    """ID of this entry in TMDB."""

    poster: str | None
    """URL to poster for this ID."""

    backdrops: list[str]
    """List of URLs for backdrops (full screen images to use as background)."""

    age_certification: str | None
    """Age rating as a string, e.g.: "R", "TV-14"."""

    scoring: Scoring | None
    """Scoring data."""

    interactions: Interactions | None
    """Interactions (likes/dislikes) data."""

    streaming_charts: StreamingCharts | None
    """JustWatch charts/ranks data."""

    offers: list[Offer]
    """List of available offers for this entry, empty if there are no available offers."""


def prepare_search_request(
    title: str, country: str, language: str, count: int, best_only: bool
) -> dict:
    """Prepare search request for JustWatch GraphQL API.
    Creates a ``GetSearchTitles`` GraphQL query.

    Country code should be two uppercase letters, however it will be auto-converted to uppercase.

    Meant to be used together with :func:`parse_search_response`.

    Args:
        title: title to search
        country: country to search for offers
        language: language of responses
        count: how many responses should be returned
        best_only: return only best offers if ``True``, return all offers if ``False``

    Returns:
        JSON/dict with GraphQL POST body
    """
    _assert_country_code_is_valid(country)
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
    Parses response for ``GetSearchTitles`` query.

    If API didn't return any data, then an empty list is returned.

    Meant to be used together with :func:`prepare_search_request`.

    Args:
        json: JSON returned by JustWatch GraphQL API

    Returns:
        Parsed received JSON as a list of ``MediaEntry`` NamedTuples
    """
    return [_parse_entry(edge["node"]) for edge in json["data"]["popularTitles"]["edges"]]


def prepare_details_request(node_id: str, country: str, language: str, best_only: bool) -> dict:
    """Prepare a details request for specified node ID to JustWatch GraphQL API.
    Creates a ``GetTitleNode`` GraphQL query.

    Country code should be two uppercase letters, however it will be auto-converted to uppercase.

    Meant to be used together with :func:`parse_details_response`.

    Args:
        node_id: node ID of entry to get details for
        country: country to search for offers
        language: language of responses
        best_only: return only best offers if ``True``, return all offers if ``False``

    Returns:
        JSON/dict with GraphQL POST body
    """
    _assert_country_code_is_valid(country)
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
    Parses response for ``GetTitleNode`` query.

    If API responded with an internal error (mostly due to not found node ID),
    then ``None`` will be returned instead.

    Meant to be used together with :func:`prepare_details_request`.

    Args:
        json: JSON returned by JustWatch GraphQL API

    Returns:
        Parsed received JSON as a ``MediaEntry`` NamedTuple,
        or ``None`` in case data for a given node ID was not found
    """
    return _parse_entry(json["data"]["node"]) if "errors" not in json else None


def prepare_offers_for_countries_request(
    node_id: str, countries: set[str], language: str, best_only: bool
) -> dict:
    """Prepare an offers request for specified node ID and for all specified countries
    to JustWatch GraphQL API.
    Creates a ``GetTitleOffers`` GraphQL query.

    Country codes should be two uppercase letters, however they will be auto-converted to uppercase.
    ``countries`` argument mustn't be empty.

    Meant to be used together with :func:`parse_offers_for_countries_response`.

    Args:
        node_id: node ID of entry to get details for
        countries: list of country codes to search for offers
        language: language of responses
        best_only: return only best offers if ``True``, return all offers if ``False``

    Returns:
        JSON/dict with GraphQL POST body
    """
    assert countries, "Cannot prepare offers request without specified countries"
    for country in countries:
        _assert_country_code_is_valid(country)
    return {
        "operationName": "GetTitleOffers",
        "variables": {
            "nodeId": node_id,
            "language": language,
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": _prepare_offers_for_countries_entry(countries),
    }


def parse_offers_for_countries_response(json: any, countries: set[str]) -> dict[str, list[Offer]]:
    """Parse response from offers query from JustWatch GraphQL API.
    Parses response for ``GetTitleOffers`` query.

    Response if searched for country codes passed as ``countries`` argument.
    Countries in JSON response which are not present in ``countries`` set will be ignored.
    If response doesn't have offers for a country, then that country still will be present
    in returned dict, just with an empty list as value.

    Meant to be used together with :func:`prepare_offers_for_countries_request`.

    Args:
        json: JSON returned by JustWatch GraphQL API
        countries: set of countries to look for in API response

    Returns:
        A dict, where keys are matching ``countries`` argument and values are offers for a given
        country parsed from JSON response.
    """
    offers_node = json["data"]["node"]
    return {
        country: list(map(_parse_offer, offers_node.get(country.upper(), [])))
        for country in countries
    }


def _assert_country_code_is_valid(code: str) -> None:
    assert len(code) == 2, f"Invalid country code: {code}, code must be 2 characters long"


def _prepare_offers_for_countries_entry(countries: set[str]) -> str:
    offer_requests = [
        _GRAPHQL_COUNTRY_OFFERS_ENTRY.format(country_code=country_code.upper())
        for country_code in countries
    ]
    main_body = _GRAPHQL_OFFERS_BY_COUNTRY_QUERY.format(country_entries="\n".join(offer_requests))
    return main_body + _GRAPHQL_OFFER_FRAGMENT


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
    tmdb_id = external_ids.get("tmdbId") if external_ids else None
    poster_url_field = content.get("posterUrl")
    poster = _IMAGES_URL + poster_url_field if poster_url_field else None
    backdrops = [_IMAGES_URL + bd.get("backdropUrl") for bd in content.get("backdrops", []) if bd]
    age_certification = content.get("ageCertification")
    scoring = _parse_scores(content.get("scoring"))
    interactions = _parse_interactions(content.get("interactions"))
    streaming_charts = _parse_streaming_charts(json)
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
        tmdb_id,
        poster,
        backdrops,
        age_certification,
        scoring,
        interactions,
        streaming_charts,
        offers,
    )


def _parse_scores(json: any) -> Scoring | None:
    if not json:
        return None
    imdb_score = json.get("imdbScore")
    imdb_votes = json.get("imdbVotes")
    tmdb_popularity = json.get("tmdbPopularity")
    tmdb_score = json.get("tmdbScore")
    tomatometer = json.get("tomatoMeter")
    certified_fresh = json.get("certifiedFresh")
    jw_rating = json.get("jwRating")
    return Scoring(
        imdb_score,
        int(imdb_votes) if imdb_votes is not None else None,
        tmdb_popularity,
        tmdb_score,
        int(tomatometer) if tomatometer is not None else None,
        certified_fresh,
        jw_rating,
    )


def _parse_interactions(json: any) -> Interactions | None:
    if not json:
        return None
    likes = json.get("likelistAdditions")
    dislikes = json.get("dislikelistAdditions")
    return Interactions(likes, dislikes)


def _parse_streaming_charts(json: any) -> StreamingCharts | None:
    if (
        not (streaming_chart_info := json.get("streamingCharts", {}).get("edges"))
        or not (streaming_chart_info := streaming_chart_info[0].get("streamingChartInfo"))
        # Getting final info is awkward, I think this in general can return a list when searching
        # for ranks for multiple entries. In this case, to unify searching and displaying details,
        # it's always getting single element in a list.
    ):
        return None
    rank = streaming_chart_info.get("rank")
    trend = streaming_chart_info.get("trend")
    trend_difference = streaming_chart_info.get("trendDifference")
    top_rank = streaming_chart_info.get("topRank")
    days_in_top_3 = streaming_chart_info.get("daysInTop3")
    days_in_top_10 = streaming_chart_info.get("daysInTop10")
    days_in_top_100 = streaming_chart_info.get("daysInTop100")
    days_in_top_1000 = streaming_chart_info.get("daysInTop1000")
    updated = streaming_chart_info.get("updatedAt")
    return StreamingCharts(
        rank,
        trend,
        trend_difference,
        top_rank,
        days_in_top_3,
        days_in_top_10,
        days_in_top_100,
        days_in_top_1000,
        updated,
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
    element_count = json.get("elementCount")
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
