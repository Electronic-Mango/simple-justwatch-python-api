"""Module storing tuples used as responses returned from this library."""

from typing import NamedTuple


class OfferPackage(NamedTuple):
    """
    Parsed single offer package from JustWatch GraphQL API for single entry.

    Contains information about platform on which given offer is available.
    """

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
    """
    Parsed single offer from JustWatch GraphQL API for single entry.

    One platform can have multiple offers for one entry available, e.g. renting, buying, etc.
    """

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
    """Trend in ranking on JustWatch, ``UP``, ``DOWN``, ``STABLE``."""

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
    """Date when rank data was last updated as a string, e.g.: ``2024-10-06T09:20:36.397Z``."""


class Episode(NamedTuple):
    """Parsed data related to a single episode."""

    episode_id: str
    """Episode ID, contains type code and numeric ID."""

    object_id: int
    """Object ID, the numeric part of full episode ID."""

    object_type: str
    """Type of entry, for episodes should be ``SHOW_EPISODE``."""

    title: str
    """Full title."""

    release_year: int
    """Release year as a number."""

    release_date: str
    """Full release date as a string, e.g. ``2013-12-16``."""

    runtime_minutes: int
    """Runtime in minutes."""

    short_description: str | None
    """Short description of this episode."""

    episode_number: int
    """Number of this episode."""

    season_number: int
    """Season number with this episode."""

    offers: list[Offer]
    """List of available offers for this episode, empty if there are no available offers."""


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

    url: str | None
    """URL to JustWatch with details for this entry."""

    release_year: int | None
    """Release year as a number."""

    release_date: str | None
    """Full release date as a string, e.g. ``2013-12-16``."""

    runtime_minutes: int
    """Runtime in minutes."""

    short_description: str | None
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

    total_season_count: int | None
    """Total season count, for non-shows it's always None."""

    total_episode_count: int | None
    """Total number of episodes in this season, for non-seasons it's always "None"."""

    season_number: int | None
    """Number of this season, for movies it's always "None"."""

    episode_number: int | None
    """Number of this episode, for non-episodes it's always "None"."""
