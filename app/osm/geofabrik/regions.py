from typing import Iterable, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from app.commons.cache import cache
from app.osm.geofabrik.collection import Collection
from app.osm.geofabrik.html_table import HtmlTable


class Regions:
    _BASE_URL_: str = 'https://download.geofabrik.de'

    @classmethod
    @cache
    def load(cls) -> pd.DataFrame:
        collection = cls._collection()
        return collection.url_tree

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
    def _fetch_tables(cls, series: Optional[pd.Series] = None) -> Iterable[pd.DataFrame]:
        url = cls._url(series=series)
        return cls._fetch_from(url=url)

    @classmethod
    @cache(sub_folder='geofabrik')
    def _fetch_from(cls, url: str) -> Iterable[pd.DataFrame]:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [cls._to_frame(html_table) for html_table in soup.findAll('table')]

    @staticmethod
    def _to_frame(table_tag: Tag) -> pd.DataFrame:
        html_table = HtmlTable(table_tag)
        return html_table.frame

    @staticmethod
    def _url(series: Optional[pd.Series], url: str = _BASE_URL_) -> str:
        if series is None:
            return url
        return f'{url}/{series["sub_region_link"]}'


if __name__ == '__main__':
    print(Regions.load())
