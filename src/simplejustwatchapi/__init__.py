"""The simplejustwatchapi package."""

from simplejustwatchapi.justwatch import details as details
from simplejustwatchapi.justwatch import episodes as episodes
from simplejustwatchapi.justwatch import offers_for_countries as offers_for_countries
from simplejustwatchapi.justwatch import search as search
from simplejustwatchapi.justwatch import seasons as seasons
from simplejustwatchapi.tuples import Episode as Episode
from simplejustwatchapi.tuples import Interactions as Interactions
from simplejustwatchapi.tuples import MediaEntry as MediaEntry
from simplejustwatchapi.tuples import Offer as Offer
from simplejustwatchapi.tuples import OfferPackage as OfferPackage
from simplejustwatchapi.tuples import Scoring as Scoring
from simplejustwatchapi.tuples import StreamingCharts as StreamingCharts

__all__ = [
    "Episode",
    "Interactions",
    "MediaEntry",
    "Offer",
    "OfferPackage",
    "Scoring",
    "StreamingCharts",
    "details",
    "episodes",
    "offers_for_countries",
    "search",
    "seasons",
]
