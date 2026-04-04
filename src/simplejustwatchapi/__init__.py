"""The main simplejustwatchapi package with "public" interface."""

from simplejustwatchapi.exceptions import (
    JustWatchApiError,
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
