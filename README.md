# Simple JustWatch Python API

[![CodeQL](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/codeql-analysis.yml)
[![Black](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/flake8.yml)
[![isort](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/isort.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/isort.yml)
[![Pytest](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml/badge.svg)](https://github.com/Electronic-Mango/simple-justwatch-python-api/actions/workflows/pytest.yml)
[![Coverage Status](https://coveralls.io/repos/github/Electronic-Mango/simple-justwatch-python-api/badge.svg?branch=main)](https://coveralls.io/github/Electronic-Mango/simple-justwatch-python-api?branch=main)
[![PyPI - Version](https://img.shields.io/pypi/v/simple-justwatch-python-api)](https://pypi.org/project/simple-justwatch-python-api/)

A simple unofficial JustWatch Python API which uses [`GraphQL`](https://graphql.org/) to access JustWatch data, built with [`httpx`](https://www.python-httpx.org/) and `Python3.11`.



## Installation

Project is available in [PyPi](https://pypi.org/project/simple-justwatch-python-api/):
```bash
pip install simple-justwatch-python-api
```



## Usage

Currently, there's only one function available - search JustWatch:
```python
from simplejustwatchapi.justwatch import search

results = search("title", "US", "en", 5, True)
```

Only the first argument is required, it specifies a title to search.

Other arguments in order are:
1. `str` country code to search for offers, have to be a 2-letter code, e.g. `US`, `GB`, `FR`, etc.
It should be uppercase, however lowercase codes are automatically converted to uppercase. By default `US` is used.
2. `str` language code, usually 2-letter lowercase code, e.g. `en`, `fr`, etc. By default `en` is used.
3. `int` how many results should be returned. Actual response can contain fewer entries if fewer are found.
By default `4` is used.
4. `bool` specify if only best offers should be returned (`True`) or all offers (`False`).
By default `True` is used.

Returned value is a list of `MediaEntry` objects:
```python
class MediaEntry(NamedTuple):
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
```

Example response:
```python
[
    MediaEntry(
        entry_id="tm10",
        object_id=10,
        object_type="MOVIE",
        title="The Matrix",
        url="https://justwatch.com/us/movie/the-matrix",
        release_year=1999,
        release_date="1999-03-30",
        genres=["scf", "act"],
        imdb_id="tt0133093",
        poster="https://images.justwatch.com/poster/140351543/s718/the-matrix.jpg",
        backdrops=[
            "https://images.justwatch.com/backdrop/104412692/s1920/the-matrix.jpg",
            "https://images.justwatch.com/backdrop/104412689/s1920/the-matrix.jpg",
            "https://images.justwatch.com/backdrop/240047406/s1920/the-matrix.jpg",
            "https://images.justwatch.com/backdrop/8668185/s1920/the-matrix.jpg",
            "https://images.justwatch.com/backdrop/104412688/s1920/the-matrix.jpg",
        ],
        offers=[
            Offer(
                monetization_type="FLATRATE",
                presentation_type="HD",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.ed68472f-1421-417d-800b-0cfdb21db71c",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="Max Amazon Channel",
                technical_name="amazonhbomax",
                icon="https://images.justwatch.com/icon/305591736/s100/amazonhbomax.{format}",
            ),
            Offer(
                monetization_type="FLATRATE",
                presentation_type="_4K",
                url="https://play.max.com/movie/012cacbd-5893-4379-b7a6-d3737c61d4b5",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="Max",
                technical_name="max",
                icon="https://images.justwatch.com/icon/305458112/s100/max.{format}",
            ),
            Offer(
                monetization_type="FLATRATE",
                presentation_type="HD",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.f11ec7df-084f-497d-8fc6-2492fad59ec7",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="AMC+ Amazon Channel",
                technical_name="amazonamcplus",
                icon="https://images.justwatch.com/icon/241732522/s100/amazonamcplus.{format}",
            ),
            Offer(
                monetization_type="FLATRATE",
                presentation_type="HD",
                url="https://therokuchannel.roku.com/details/e981c230598059f2bf41f94156700488/the-matrix?source=bing",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="AMC+ Roku Premium Channel",
                technical_name="rokuchannelamcplus",
                icon="https://images.justwatch.com/icon/252888472/s100/rokuchannelamcplus.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://tv.apple.com/us/movie/the-matrix/umc.cmc.af8k9kcq9r1s1qmmdxpq4itn?playableId=tvs.sbd.9001%3A271469518",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Apple TV",
                technical_name="itunes",
                icon="https://images.justwatch.com/icon/190848813/s100/itunes.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.ed68472f-1421-417d-800b-0cfdb21db71c",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Amazon Video",
                technical_name="amazon",
                icon="https://images.justwatch.com/icon/430993/s100/amazon.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://play.google.com/store/movies/details/The_Matrix?gl=US&hl=en&id=ilPevtGe57s.P",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Google Play Movies",
                technical_name="play",
                icon="https://images.justwatch.com/icon/169478387/s100/play.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.youtube.com/results?search_query=The+Matrix%2Bmovie",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="YouTube",
                technical_name="youtube",
                icon="https://images.justwatch.com/icon/59562423/s100/youtube.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.vudu.com/content/movies/details/The-Matrix/9254",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Vudu",
                technical_name="vudu",
                icon="https://images.justwatch.com/icon/249324969/s100/vudu.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.microsoft.com/en-us/p/the-matrix/8d6kgwzl5r09",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Microsoft Store",
                technical_name="microsoft",
                icon="https://images.justwatch.com/icon/820542/s100/microsoft.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.directv.com/movies/The-Matrix-ZUF5bGQvemdYeVJ2L3lpNERBQ205QT09",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="DIRECTV",
                technical_name="directv",
                icon="https://images.justwatch.com/icon/158260222/s100/directv.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="HD",
                url="https://ondemand.spectrum.net/movies/22804/the-matrix/",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Spectrum On Demand",
                technical_name="spectrumondemand",
                icon="https://images.justwatch.com/icon/305635208/s100/spectrumondemand.{format}",
            ),
            Offer(
                monetization_type="BUY",
                presentation_type="HD",
                url="http://www.amctheatres.com/movies/the-matrix-4111",
                price_string="$14.99",
                price_value=14.99,
                price_currency="USD",
                name="AMC on Demand",
                technical_name="amctheatresondemand",
                icon="https://images.justwatch.com/icon/166008757/s100/amctheatresondemand.{format}",
            ),
        ],
    ),
    MediaEntry(
        entry_id="tm827124",
        object_id=827124,
        object_type="MOVIE",
        title="The Matrix Resurrections",
        url="https://justwatch.com/us/movie/the-matrix-resurrections",
        release_year=2021,
        release_date="2021-12-16",
        genres=["act", "scf"],
        imdb_id="tt10838180",
        poster="https://images.justwatch.com/poster/257943908/s718/the-matrix-resurrections.jpg",
        backdrops=[
            "https://images.justwatch.com/backdrop/245633536/s1920/the-matrix-resurrections.jpg",
            "https://images.justwatch.com/backdrop/257943910/s1920/the-matrix-resurrections.jpg",
            "https://images.justwatch.com/backdrop/257943914/s1920/the-matrix-resurrections.jpg",
            "https://images.justwatch.com/backdrop/256148705/s1920/the-matrix-resurrections.jpg",
            "https://images.justwatch.com/backdrop/257380502/s1920/the-matrix-resurrections.jpg",
        ],
        offers=[
            Offer(
                monetization_type="FLATRATE",
                presentation_type="HD",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.bd6bd6ed-93ce-41f7-a06d-3a1277b94fcb",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="Max Amazon Channel",
                technical_name="amazonhbomax",
                icon="https://images.justwatch.com/icon/305591736/s100/amazonhbomax.{format}",
            ),
            Offer(
                monetization_type="FLATRATE",
                presentation_type="_4K",
                url="https://play.max.com/movie/a553a6c7-66a0-42fc-8f6a-a47f926fe435",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="Max",
                technical_name="max",
                icon="https://images.justwatch.com/icon/305458112/s100/max.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.bd6bd6ed-93ce-41f7-a06d-3a1277b94fcb",
                price_string="$3.79",
                price_value=3.79,
                price_currency="USD",
                name="Amazon Video",
                technical_name="amazon",
                icon="https://images.justwatch.com/icon/430993/s100/amazon.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://tv.apple.com/us/movie/the-matrix-resurrections/umc.cmc.1xfut1sq2hvb9faupyabxog7q?playableId=tvs.sbd.9001%3A1595166379",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Apple TV",
                technical_name="itunes",
                icon="https://images.justwatch.com/icon/190848813/s100/itunes.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://play.google.com/store/movies/details/The_Matrix_Resurrections?gl=US&hl=en&id=aoFm38NvOCY.P",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Google Play Movies",
                technical_name="play",
                icon="https://images.justwatch.com/icon/169478387/s100/play.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.youtube.com/results?search_query=The+Matrix+Resurrections%2Bmovie",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="YouTube",
                technical_name="youtube",
                icon="https://images.justwatch.com/icon/59562423/s100/youtube.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.vudu.com/content/movies/details/The-Matrix-Resurrections/1907631",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Vudu",
                technical_name="vudu",
                icon="https://images.justwatch.com/icon/249324969/s100/vudu.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.microsoft.com/en-us/p/the-matrix-resurrections/8d6kgwxn5rlr",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Microsoft Store",
                technical_name="microsoft",
                icon="https://images.justwatch.com/icon/820542/s100/microsoft.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.directv.com/movies/The-Matrix-Resurrections-VDhidUx4QXRCTGw5M2wzditEMVM4QT09",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="DIRECTV",
                technical_name="directv",
                icon="https://images.justwatch.com/icon/158260222/s100/directv.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="HD",
                url="https://ondemand.spectrum.net/movies/18062455/the-matrix-resurrections/",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Spectrum On Demand",
                technical_name="spectrumondemand",
                icon="https://images.justwatch.com/icon/305635208/s100/spectrumondemand.{format}",
            ),
            Offer(
                monetization_type="BUY",
                presentation_type="HD",
                url="http://www.amctheatres.com/movies/the-matrix-resurrections-62603",
                price_string="$14.99",
                price_value=14.99,
                price_currency="USD",
                name="AMC on Demand",
                technical_name="amctheatresondemand",
                icon="https://images.justwatch.com/icon/166008757/s100/amctheatresondemand.{format}",
            ),
        ],
    ),
    MediaEntry(
        entry_id="tm11",
        object_id=11,
        object_type="MOVIE",
        title="The Matrix Reloaded",
        url="https://justwatch.com/us/movie/the-matrix-2-reloaded",
        release_year=2003,
        release_date="2003-05-15",
        genres=["trl", "scf", "act"],
        imdb_id="tt0234215",
        poster="https://images.justwatch.com/poster/251725999/s718/the-matrix-2-reloaded.jpg",
        backdrops=[
            "https://images.justwatch.com/backdrop/8721510/s1920/the-matrix-2-reloaded.jpg",
            "https://images.justwatch.com/backdrop/300681582/s1920/the-matrix-2-reloaded.jpg",
            "https://images.justwatch.com/backdrop/186039261/s1920/the-matrix-2-reloaded.jpg",
            "https://images.justwatch.com/backdrop/8721517/s1920/the-matrix-2-reloaded.jpg",
            "https://images.justwatch.com/backdrop/8721516/s1920/the-matrix-2-reloaded.jpg",
        ],
        offers=[
            Offer(
                monetization_type="FLATRATE",
                presentation_type="HD",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.c19d194f-3fed-4960-ad7b-727e72672f33",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="Max Amazon Channel",
                technical_name="amazonhbomax",
                icon="https://images.justwatch.com/icon/305591736/s100/amazonhbomax.{format}",
            ),
            Offer(
                monetization_type="FLATRATE",
                presentation_type="_4K",
                url="https://play.max.com/movie/15f1f852-5a97-4e78-b509-e045dbc1ba37",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="Max",
                technical_name="max",
                icon="https://images.justwatch.com/icon/305458112/s100/max.{format}",
            ),
            Offer(
                monetization_type="FLATRATE",
                presentation_type="HD",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.98abdb4d-6a62-48e1-b04e-28e76d519311",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="AMC+ Amazon Channel",
                technical_name="amazonamcplus",
                icon="https://images.justwatch.com/icon/241732522/s100/amazonamcplus.{format}",
            ),
            Offer(
                monetization_type="FLATRATE",
                presentation_type="HD",
                url="https://therokuchannel.roku.com/details/9e0cb3c5c86051e18be046a12b5b19b8/the-matrix-reloaded?source=bing",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="AMC+ Roku Premium Channel",
                technical_name="rokuchannelamcplus",
                icon="https://images.justwatch.com/icon/252888472/s100/rokuchannelamcplus.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://tv.apple.com/us/movie/the-matrix-reloaded/umc.cmc.5b3qv27alugfj95rrag186slh?playableId=tvs.sbd.9001%3A283218560",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Apple TV",
                technical_name="itunes",
                icon="https://images.justwatch.com/icon/190848813/s100/itunes.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.c19d194f-3fed-4960-ad7b-727e72672f33",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Amazon Video",
                technical_name="amazon",
                icon="https://images.justwatch.com/icon/430993/s100/amazon.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://play.google.com/store/movies/details/The_Matrix_Reloaded?gl=US&hl=en&id=uRVdSV8nBzw.P",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Google Play Movies",
                technical_name="play",
                icon="https://images.justwatch.com/icon/169478387/s100/play.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.youtube.com/results?search_query=The+Matrix+Reloaded%2Bmovie",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="YouTube",
                technical_name="youtube",
                icon="https://images.justwatch.com/icon/59562423/s100/youtube.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.vudu.com/content/movies/details/The-Matrix-Reloaded/10678",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Vudu",
                technical_name="vudu",
                icon="https://images.justwatch.com/icon/249324969/s100/vudu.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.microsoft.com/en-us/p/the-matrix-reloaded/8d6kgwzl5hmr",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Microsoft Store",
                technical_name="microsoft",
                icon="https://images.justwatch.com/icon/820542/s100/microsoft.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.directv.com/movies/The-Matrix-Reloaded-NXJOdzBaRTBoSFF0dWc5UU5Ramg5Zz09",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="DIRECTV",
                technical_name="directv",
                icon="https://images.justwatch.com/icon/158260222/s100/directv.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="HD",
                url="https://ondemand.spectrum.net/movies/31912/the-matrix-reloaded/",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Spectrum On Demand",
                technical_name="spectrumondemand",
                icon="https://images.justwatch.com/icon/305635208/s100/spectrumondemand.{format}",
            ),
            Offer(
                monetization_type="BUY",
                presentation_type="HD",
                url="http://www.amctheatres.com/movies/the-matrix-reloaded-5505",
                price_string="$4.99",
                price_value=4.99,
                price_currency="USD",
                name="AMC on Demand",
                technical_name="amctheatresondemand",
                icon="https://images.justwatch.com/icon/166008757/s100/amctheatresondemand.{format}",
            ),
        ],
    ),
    MediaEntry(
        entry_id="tm12",
        object_id=12,
        object_type="MOVIE",
        title="The Matrix Revolutions",
        url="https://justwatch.com/us/movie/the-matrix-revolutions",
        release_year=2003,
        release_date="2003-11-05",
        genres=["trl", "scf", "act"],
        imdb_id="tt0242653",
        poster="https://images.justwatch.com/poster/179166803/s718/the-matrix-revolutions.jpg",
        backdrops=[
            "https://images.justwatch.com/backdrop/8721981/s1920/the-matrix-revolutions.jpg",
            "https://images.justwatch.com/backdrop/8721983/s1920/the-matrix-revolutions.jpg",
            "https://images.justwatch.com/backdrop/203549468/s1920/the-matrix-revolutions.jpg",
            "https://images.justwatch.com/backdrop/8721987/s1920/the-matrix-revolutions.jpg",
            "https://images.justwatch.com/backdrop/205405481/s1920/the-matrix-revolutions.jpg",
        ],
        offers=[
            Offer(
                monetization_type="FLATRATE",
                presentation_type="HD",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.e390b59a-d138-45f8-9305-8806a4bcb984",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="Max Amazon Channel",
                technical_name="amazonhbomax",
                icon="https://images.justwatch.com/icon/305591736/s100/amazonhbomax.{format}",
            ),
            Offer(
                monetization_type="FLATRATE",
                presentation_type="_4K",
                url="https://play.max.com/movie/7f34ec0d-34d9-42bb-96ac-251a42009f2d",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="Max",
                technical_name="max",
                icon="https://images.justwatch.com/icon/305458112/s100/max.{format}",
            ),
            Offer(
                monetization_type="FLATRATE",
                presentation_type="HD",
                url="https://therokuchannel.roku.com/details/c9f116b03d8f5cea976aefb5490a4aec/the-matrix-revolutions?source=bing",
                price_string=None,
                price_value=None,
                price_currency="USD",
                name="AMC+ Roku Premium Channel",
                technical_name="rokuchannelamcplus",
                icon="https://images.justwatch.com/icon/252888472/s100/rokuchannelamcplus.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://tv.apple.com/us/movie/the-matrix-revolutions/umc.cmc.52it1gdofstjm0glh3upzjjz5?playableId=tvs.sbd.9001%3A271469065",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Apple TV",
                technical_name="itunes",
                icon="https://images.justwatch.com/icon/190848813/s100/itunes.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://watch.amazon.com/detail?gti=amzn1.dv.gti.e390b59a-d138-45f8-9305-8806a4bcb984",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Amazon Video",
                technical_name="amazon",
                icon="https://images.justwatch.com/icon/430993/s100/amazon.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://play.google.com/store/movies/details/The_Matrix_Revolutions?gl=us&hl=en&id=7AnXDfqMMHc.P",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Google Play Movies",
                technical_name="play",
                icon="https://images.justwatch.com/icon/169478387/s100/play.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.youtube.com/results?search_query=The+Matrix+Revolutions%2Bmovie",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="YouTube",
                technical_name="youtube",
                icon="https://images.justwatch.com/icon/59562423/s100/youtube.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.vudu.com/content/movies/details/The-Matrix-Revolutions/9986",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Vudu",
                technical_name="vudu",
                icon="https://images.justwatch.com/icon/249324969/s100/vudu.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.microsoft.com/en-us/p/the-matrix-revolutions/8d6kgwzl6568",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Microsoft Store",
                technical_name="microsoft",
                icon="https://images.justwatch.com/icon/820542/s100/microsoft.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="_4K",
                url="https://www.directv.com/movies/The-Matrix-Revolutions-R2ZTV0Z1dndSeU95SkdQODAwVWF4UT09",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="DIRECTV",
                technical_name="directv",
                icon="https://images.justwatch.com/icon/158260222/s100/directv.{format}",
            ),
            Offer(
                monetization_type="RENT",
                presentation_type="HD",
                url="https://ondemand.spectrum.net/movies/33157/the-matrix-revolutions/",
                price_string="$3.99",
                price_value=3.99,
                price_currency="USD",
                name="Spectrum On Demand",
                technical_name="spectrumondemand",
                icon="https://images.justwatch.com/icon/305635208/s100/spectrumondemand.{format}",
            ),
            Offer(
                monetization_type="BUY",
                presentation_type="HD",
                url="http://www.amctheatres.com/movies/the-matrix-revolutions-5509",
                price_string="$14.99",
                price_value=14.99,
                price_currency="USD",
                name="AMC on Demand",
                technical_name="amctheatresondemand",
                icon="https://images.justwatch.com/icon/166008757/s100/amctheatresondemand.{format}",
            ),
        ],
    ),
]
```
You can replace `.{format}` in icon URLs with whatever format you want - `.jpg`, `.png`, `.ico`, most of them should work.
The same applies to poster and backdrop URLs - you can replace `.jpg` extension with `.png`, etc.



## Disclaimer

This API is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with JustWatch.
This is an independent and unofficial project.
Use at your own risk.
