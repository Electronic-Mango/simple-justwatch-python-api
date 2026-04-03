"""
Module responsible for creating GraphQL queries and parsing responses from JustWatch.

Parsed responses are returned as Python NamedTuples for easier access.
"""

from typing import Any

from simplejustwatchapi.exceptions import (
    JustWatchApiError,
    JustWatchCountryCodeError,
    JustWatchError,
)
from simplejustwatchapi.graphql import (
    graphql_details_query,
    graphql_episodes_query,
    graphql_offers_for_countries_query,
    graphql_popular_query,
    graphql_providers_query,
    graphql_search_query,
    graphql_seasons_query,
)
from simplejustwatchapi.tuples import (
    Episode,
    Interactions,
    MediaEntry,
    Offer,
    OfferPackage,
    Scoring,
    StreamingCharts,
)

_DETAILS_URL = "https://justwatch.com"
_IMAGES_URL = "https://images.justwatch.com"
_COUNTRY_CODE_LENGTH = 2


def prepare_search_request(
    title: str,
    country: str,
    language: str,
    count: int,
    best_only: bool,
    offset: int,
    providers: list[str] | str | None,
) -> dict:
    """
    Prepare search request for JustWatch GraphQL API.

    Creates a ``GetSearchTitles`` GraphQL query.

    Country code should be two uppercase letters, however it will be auto-converted to
    uppercase.

    Meant to be used together with :func:`parse_search_response`.

    Args:
        title (str): Title to search.
        country (str): Country to search for offers.
        language (str): Language of responses.
        count (int): How many responses should be returned.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.
        offset (int): Search results offset.
        providers (list[str] | str | None): 3-letter service identifier(s),
            or `None` for all providers.

    Returns:
        (dict): JSON/`dict` with GraphQL POST body.

    Raises:
        exceptions.JustWatchCountryCodeError: Provided `country` is not a 2-letter code.

    """
    _raise_for_invalid_country_code(country)
    return {
        "operationName": "GetSearchTitles",
        "variables": {
            "first": count,
            "searchTitlesFilter": {"searchQuery": title, "packages": providers},
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
            "offset": offset or None,
        },
        "query": graphql_search_query(),
    }


def parse_search_response(json: dict) -> list[MediaEntry]:
    """
    Parse response from search query from JustWatch GraphQL API.

    Parses response for `GetSearchTitles` query.

    If API didn't return any data, then an empty list is returned.

    Meant to be used together with [`prepare_search_request`]
    [simplejustwatchapi.query.prepare_search_request].

    Args:
        json (dict): JSON returned by JustWatch GraphQL API.

    Returns:
        (list[MediaEntry)]: Parsed received JSON as a list of `MediaEntry` NamedTuples.

    Raises:
        exceptions.JustWatchApiError: Response from API has internal errors.

    """
    _raise_for_errors_in_response(json)
    return [
        _parse_entry(edge["node"]) for edge in json["data"]["popularTitles"]["edges"]
    ]


def prepare_popular_request(
    country: str,
    language: str,
    count: int,
    best_only: bool,
    offset: int,
    providers: list[str] | str | None,
) -> dict:
    """
    Prepare "get popular" request for JustWatch GraphQL API.

    Creates a ``GetPopularTitles`` GraphQL query.

    Country code should be two uppercase letters, however it will be auto-converted to
    uppercase.

    Meant to be used together with [`parse_popular_response`]
    [simplejustwatchapi.query.parse_popular_response].

    Args:
        country (str): Country to search for offers.
        language (str): Language of responses.
        count (int): How many responses should be returned.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.
        offset (int): Search results offset.
        providers (list[str] | str | None): 3-letter service identifier(s),
            or `None` for all providers.

    Returns:
        (dict): JSON/`dict` with GraphQL POST body.

    Raises:
        exceptions.JustWatchCountryCodeError: Provided `country` is not a 2-letter code.

    """
    _raise_for_invalid_country_code(country)
    return {
        "operationName": "GetPopularTitles",
        "variables": {
            "first": count,
            "popularTitlesFilter": {"packages": providers},
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
            "offset": offset or None,
        },
        "query": graphql_popular_query(),
    }


def parse_popular_response(json: dict) -> list[MediaEntry]:
    """
    Parse response from the "get popular" query from JustWatch GraphQL API.

    Parses response for `GetPopularTitles` query.

    If API didn't return any data, then an empty list is returned.

    Meant to be used together with [`prepare_popular_request`]
    [simplejustwatchapi.query.prepare_popular_request].

    Args:
        json (dict): JSON returned by JustWatch GraphQL API.

    Returns:
        (list[MediaEntry]): Parsed received JSON as a list of `MediaEntry` NamedTuples.

    Raises:
        exceptions.JustWatchApiError: Response from API has internal errors.

    """
    _raise_for_errors_in_response(json)
    return [
        _parse_entry(edge["node"]) for edge in json["data"]["popularTitles"]["edges"]
    ]


def prepare_details_request(
    node_id: str, country: str, language: str, best_only: bool
) -> dict:
    """
    Prepare a details request for specified node ID to JustWatch GraphQL API.

    Creates a `GetTitleNode` GraphQL query.

    Country code should be two uppercase letters, however it will be auto-converted to
    uppercase.

    Meant to be used together with [`parse_details_response`]
    [simplejustwatchapi.query.parse_details_response].

    Args:
        node_id (str): Node ID of entry to get details for.
        country (str): Country to search for offers.
        language (str): Language of responses.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.

    Returns:
        (dict): JSON/`dict` with GraphQL POST body.

    Raises:
        exceptions.JustWatchCountryCodeError: Provided `country` is not a 2-letter code.

    """
    _raise_for_invalid_country_code(country)
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
        "query": graphql_details_query(),
    }


def parse_details_response(json: dict) -> MediaEntry:
    """
    Parse response from details query from JustWatch GraphQL API.

    Parses response for `GetTitleNode` query.

    Meant to be used together with [`prepare_details_request`]
    [simplejustwatchapi.query.prepare_details_request].

    Args:
        json (dict): JSON returned by JustWatch GraphQL API.

    Returns:
        (MediaEntry): Parsed received JSON as a `MediaEntry` NamedTuple.

    Raises:
        exceptions.JustWatchApiError: Response from API has internal errors.

    """
    _raise_for_errors_in_response(json)
    return _parse_entry(json["data"]["node"])


def prepare_seasons_request(
    show_id: str, country: str, language: str, best_only: bool
) -> dict:
    """
    Prepare a seasons details request for specified show ID to JustWatch GraphQL API.

    Creates a `GetTitleNode` GraphQL query.

    Country code should be two uppercase letters, however it will be auto-converted to
    uppercase.

    Meant to be used together with [`parse_seasons_response`]
    [simplejustwatchapi.query.parse_seasons_response].

    Args:
        show_id (str): Show ID of entry to get details for.
        country (str): Country to search for offers.
        language (str): Language of responses.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.

    Returns:
        (dict): JSON/`dict` with GraphQL POST body.

    Raises:
        exceptions.JustWatchCountryCodeError: Provided `country` is not a 2-letter code.

    """
    _raise_for_invalid_country_code(country)
    return {
        "operationName": "GetTitleNode",
        "variables": {
            "nodeId": show_id,
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": graphql_seasons_query(),
    }


def parse_seasons_response(json: dict) -> list[MediaEntry]:
    """
    Parse response from seasons details query from JustWatch GraphQL API.

    Parses response for `GetTitleNode` query.

    Meant to be used together with [`prepare_seasons_request`]
    [simplejustwatchapi.query.prepare_seasons_request].

    Args:
        json (dict): JSON returned by JustWatch GraphQL API.

    Returns:
        (list[MediaEntry]): Parsed received JSON as a `MediaEntry` NamedTuple list.

    Raises:
        exceptions.JustWatchApiError: Response from API has internal errors.

    """
    _raise_for_errors_in_response(json)
    return [_parse_entry(season) for season in json["data"]["node"].get("seasons", [])]


def prepare_episodes_request(
    episode_id: str, country: str, language: str, best_only: bool
) -> dict:
    """
    Prepare a episodes details request for specified node ID to JustWatch GraphQL API.

    Creates a `GetTitleNode` GraphQL query.

    Country code should be two uppercase letters, however it will be auto-converted to
    uppercase.

    Meant to be used together with [`parse_episodes_response`]
    [simplejustwatchapi.query.parse_episodes_response].

    Args:
        episode_id (str): Episode ID of entry to get details for.
        country (str): Country to search for offers.
        language (str): Language of responses.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.

    Returns:
        (dict): JSON/`dict` with GraphQL POST body.

    Raises:
        exceptions.JustWatchCountryCodeError: Provided `country` is not a 2-letter code.

    """
    _raise_for_invalid_country_code(country)
    return {
        "operationName": "GetTitleNode",
        "variables": {
            "nodeId": episode_id,
            "language": language,
            "country": country.upper(),
            "formatPoster": "JPG",
            "formatOfferIcon": "PNG",
            "profile": "S718",
            "backdropProfile": "S1920",
            "filter": {"bestOnly": best_only},
        },
        "query": graphql_episodes_query(),
    }


def parse_episodes_response(json: dict) -> list[Episode]:
    """
    Parse response from episodes details query from JustWatch GraphQL API.

    Parses response for `GetTitleNode` query.

    Meant to be used together with [`prepare_episodes_request`]
    [simplejustwatchapi.query.prepare_episodes_request].

    Args:
        json (dict): JSON returned by JustWatch GraphQL API.

    Returns:
        (list[Episode]): Parsed received JSON as a `Episode` NamedTuple list.

    Raises:
        exceptions.JustWatchApiError: Response from API has internal errors.

    """
    _raise_for_errors_in_response(json)
    return [
        _parse_episode(episode) for episode in json["data"]["node"].get("episodes", [])
    ]


def prepare_offers_for_countries_request(
    node_id: str,
    countries: set[str],
    language: str,
    best_only: bool,
) -> dict:
    """
    Prepare an offers request for the node ID and for all given countries.

    Creates a `GetTitleOffers` GraphQL query.

    Country codes should be two uppercase letters, however they will be auto-converted
    to uppercase. `countries` argument must not be empty.

    Meant to be used together with [`parse_offers_for_countries_response`]
    [simplejustwatchapi.query.parse_offers_for_countries_response].

    Args:
        node_id (str): Node ID of entry to get details for.
        countries (set[str]): Set of country codes to search for offers.
        language (str): Language of responses.
        best_only (bool): Return only best offers if `True`,
            return all offers if `False`.

    Returns:
        (dict): JSON/`dict` with GraphQL POST body.

    Raises:
        exceptions.JustWatchCountryCodeError: Provided `countries` contain invalid
            country code.

    """
    if not countries:
        # This should never happen, justwatch.py should take care of this.
        # If it will happen API will respond with an error due to unused variables.
        error_msg = "No country codes, should not happen!"
        raise JustWatchError(error_msg)
    for country in countries:
        _raise_for_invalid_country_code(country)
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
        "query": graphql_offers_for_countries_query(countries),
    }


def parse_offers_for_countries_response(
    json: dict, countries: set[str]
) -> dict[str, list[Offer]]:
    """
    Parse response from offers query from JustWatch GraphQL API.

    Parses response for `GetTitleOffers` query.

    Response if searched for country codes passed as `countries` argument.
    Countries in JSON response which are not present in `countries` set will be ignored.
    If response doesn't have offers for a country, then that country still will be
    present in returned dict, just with an empty list as value.

    Meant to be used together with [`prepare_offers_for_countries_request`]
    [simplejustwatchapi.query.prepare_offers_for_countries_request].

    Args:
        json (dict): JSON returned by JustWatch GraphQL API.
        countries (set[str]): Set of country codes to look for in API response.

    Returns:
        (dict[str, list[Offer]]): A `dict`, where keys are matching `countries` argument
            and values are offers for a given country parsed from JSON response.

    Raises:
        exceptions.JustWatchApiError: Response from API has internal errors.

    """
    _raise_for_errors_in_response(json)
    return {
        country: list(map(_parse_offer, json["data"]["node"].get(country.upper(), [])))
        for country in countries
    }


def prepare_providers_request(country: str) -> dict:
    """
    Prepare "get all providers" request for JustWatch GraphQL API.

    Creates a `GetProviders` GraphQL query.

    Country code should be two uppercase letters, however it will be auto-converted to
    uppercase.

    Meant to be used together with [`parse_providers_response`]
    [simplejustwatchapi.query.parse_providers_response].

    Args:
        country (str): 2-letter country code for which providers should be looked up.

    Returns:
        (dict): JSON/`dict` with GraphQL POST body.

    Raises:
        exceptions.JustWatchCountryCodeError: Provided `country` is not a 2-letter code.

    """
    _raise_for_invalid_country_code(country)
    return {
        "operationName": "GetProviders",
        "variables": {
            "country": country.upper(),
            "formatOfferIcon": "PNG",
        },
        "query": graphql_providers_query(),
    }


def parse_providers_response(json: dict) -> list[OfferPackage]:
    """
    Parse response from "get all providers" query from JustWatch GraphQL API.

    Parses response for `GetProviders` query.

    If API didn't return any data, then an empty list is returned.

    Meant to be used together with [`prepare_providers_request`]
    [simplejustwatchapi.query.prepare_providers_request].

    Args:
        json (dict): JSON returned by JustWatch GraphQL API.

    Returns:
        (list[OfferPackage]): Parsed received JSON as a list of `OfferPackage`.

    Raises:
        exceptions.JustWatchApiError: Response from API has internal errors.

    """
    _raise_for_errors_in_response(json)
    return [_parse_package(package) for package in json["data"]["packages"]]


def _raise_for_invalid_country_code(code: str) -> None:
    if len(code) != _COUNTRY_CODE_LENGTH:
        raise JustWatchCountryCodeError(code)


def _raise_for_errors_in_response(json: dict) -> None:
    if "errors" in json:
        raise JustWatchApiError(json["errors"])


def _parse_entry(json: Any) -> MediaEntry:
    entry_id = json.get("id")
    object_id = json.get("objectId")
    object_type = json.get("objectType")
    total_episode_count = json.get("totalEpisodeCount")
    content = json["content"]
    season_number = content.get("seasonNumber")
    episode_number = content.get("episodeNumber")
    title = content.get("title")
    url_field = content.get("fullPath")
    # Missing URL should be "None", not an empty string,
    # but I want to keep the MediaEntry structure unchanged for now.
    url = _DETAILS_URL + url_field if url_field else ""
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
    backdrops = [
        _IMAGES_URL + backdrop.get("backdropUrl")
        for backdrop in content.get("backdrops", [])
        if backdrop
    ]
    age_certification = content.get("ageCertification")
    scoring = _parse_scores(content.get("scoring"))
    interactions = _parse_interactions(content.get("interactions"))
    streaming_charts = _parse_streaming_charts(json)
    offers = [_parse_offer(offer) for offer in json.get("offers", []) if offer]
    total_season_count = json.get("totalSeasonCount")
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
        total_season_count,
        total_episode_count,
        season_number,
        episode_number,
    )


def _parse_episode(json: Any) -> Episode:
    episode_id = json.get("id")
    object_id = json.get("objectId")
    object_type = json.get("objectType")
    content = json["content"]
    title = content.get("title")
    year = content.get("originalReleaseYear")
    date = content.get("originalReleaseDate")
    runtime_minutes = content.get("runtime")
    short_description = content.get("shortDescription")
    episode_number = content.get("episodeNumber")
    season_number = content.get("seasonNumber")
    offers = [_parse_offer(offer) for offer in json.get("offers", []) if offer]
    return Episode(
        episode_id,
        object_id,
        object_type,
        title,
        year,
        date,
        runtime_minutes,
        short_description,
        episode_number,
        season_number,
        offers,
    )


def _parse_scores(json: Any) -> Scoring | None:
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


def _parse_interactions(json: Any) -> Interactions | None:
    if not json:
        return None
    likes = json.get("likelistAdditions")
    dislikes = json.get("dislikelistAdditions")
    return Interactions(likes, dislikes)


def _parse_streaming_charts(json: Any) -> StreamingCharts | None:
    if (
        not (chart_info := json.get("streamingCharts", {}).get("edges"))
        or not (chart_info := chart_info[0].get("streamingChartInfo"))
        # Getting final info is awkward, I think this in general can return a list when
        # searching for ranks for multiple entries. In this case, to unify searching
        # and displaying details, it's always getting single element in a list.
    ):
        return None
    rank = chart_info.get("rank")
    trend = chart_info.get("trend")
    trend_difference = chart_info.get("trendDifference")
    top_rank = chart_info.get("topRank")
    days_in_top_3 = chart_info.get("daysInTop3")
    days_in_top_10 = chart_info.get("daysInTop10")
    days_in_top_100 = chart_info.get("daysInTop100")
    days_in_top_1000 = chart_info.get("daysInTop1000")
    updated = chart_info.get("updatedAt")
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


def _parse_offer(json: Any) -> Offer:
    offer_id = json.get("id")
    monetization_type = json.get("monetizationType")
    presentation_type = json.get("presentationType")
    price_string = json.get("retailPrice")
    price_value = json.get("retailPriceValue")
    price_currency = json.get("currency")
    last_change_retail_price_value = json.get("lastChangeRetailPriceValue")
    offer_type = json.get("type")
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
        offer_id,
        monetization_type,
        presentation_type,
        price_string,
        price_value,
        price_currency,
        last_change_retail_price_value,
        offer_type,
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


def _parse_package(json: Any) -> OfferPackage:
    platform_id = json.get("id")
    package_id = json.get("packageId")
    name = json.get("clearName")
    technical_name = json.get("technicalName")
    short_name = json.get("shortName")
    icon = _IMAGES_URL + json.get("icon")
    return OfferPackage(platform_id, package_id, name, technical_name, short_name, icon)
