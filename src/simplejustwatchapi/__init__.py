"""The main simplejustwatchapi package with "public" interface."""

from simplejustwatchapi.exceptions import (
    JustWatchApiError,
    JustWatchCountryCodeError,
    JustWatchError,
    JustWatchHttpError,
)
from simplejustwatchapi.justwatch import (
    details,
    episodes,
    offers_for_countries,
    popular,
    providers,
    search,
    seasons,
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

__all__ = [
    "Episode",
    "Interactions",
    "JustWatchApiError",
    "JustWatchCountryCodeError",
    "JustWatchError",
    "JustWatchHttpError",
    "MediaEntry",
    "Offer",
    "OfferPackage",
    "Scoring",
    "StreamingCharts",
    "details",
    "episodes",
    "offers_for_countries",
    "popular",
    "providers",
    "search",
    "seasons",
]
