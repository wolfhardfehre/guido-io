from pathlib import Path
from typing import Union, Iterable

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

from app.osm.available_zones.collection import Collection
from app.osm.available_zones.html_table import HtmlTable
from app.paths import CACHE_PATH


class AvailableZones:
    FILE_PATH: Path = CACHE_PATH / 'available_zones.csv'
    BASE_URL: str = 'https://download.geofabrik.de'

    @classmethod
    def fetch(cls, file_path: Union[Path, None] = FILE_PATH) -> pd.DataFrame:
        collection = cls._collection()
        url_tree = collection.url_tree
        url_tree.to_csv(file_path, index=False)
        return url_tree

    @classmethod
    def _collection(cls) -> Collection:
        collection = Collection()
        for continents in cls._fetch_tables():
            collection = cls._add_continents(collection=collection, continents=continents)
        return collection

    @classmethod
    def _add_continents(cls, collection: Collection, continents: pd.DataFrame) -> Collection:
        for _, continent in continents.iterrows():
            collection.continent = continent
            collection = cls._add_continent(collection=collection)
        return collection

    @classmethod
    def _add_continent(cls, collection: Collection) -> Collection:
        for countries in cls._fetch_tables(collection.continent):
            if 'file_link' in countries.columns:
                continue
            countries['continent'] = collection.continent['sub_region']
            countries['continent_link'] = collection.continent['download_link']
            countries['country'] = countries['sub_region']
            countries['country_link'] = countries['download_link']
            collection = cls._add_countries(collection=collection, countries=countries)
        return collection

    @classmethod
    def _add_countries(cls, collection: Collection, countries: pd.DataFrame) -> Collection:
        collection.countries_to_drop = []
        for _, country in countries.iterrows():
            collection = cls._add_states(collection=collection, country=country)
        countries = countries[~countries['country'].isin(collection.countries_to_drop)]
        collection.frames.append(countries)
        return collection

    @classmethod
    def _add_states(cls, collection: Collection, country: pd.Series) -> Collection:
        for states in cls._fetch_tables(country):
            if 'file_link' in states.columns:
                continue
            states['continent'] = collection.continent['sub_region']
            states['continent_link'] = collection.continent['download_link']
            states['country'] = country['sub_region']
            states['country_link'] = country['download_link']
            states['state'] = states['sub_region']
            states['state_link'] = states['download_link']
            collection.frames.append(states)
            collection.countries_to_drop.append(country['sub_region'])
        return collection

    @classmethod
    def _fetch_tables(cls, series: Union[pd.Series, None] = None) -> Iterable[pd.DataFrame]:
        url = cls._url(series=series)
        return cls._fetch_from(url=url)

    @classmethod
    def _fetch_from(cls, url: str) -> Iterable[pd.DataFrame]:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [cls._to_frame(html_table) for html_table in soup.findAll('table')]

    @staticmethod
    def _to_frame(table_tag: Tag) -> pd.DataFrame:
        html_table = HtmlTable(table_tag)
        return html_table.frame

    @staticmethod
    def _url(series: Union[pd.Series, None], url: str = BASE_URL) -> str:
        if series is None:
            return url
        return f'{url}/{series["sub_region_link"]}'
