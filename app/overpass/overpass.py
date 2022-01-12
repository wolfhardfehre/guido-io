import logging
import os

import requests
import pandas as pd
from app.paths import CACHE_PATH
from app.commons.hashing import md5_hash
from app.overpass.location import Location


class Overpass:
    """
    Example query: http://overpass-api.de/api/interpreter?data=
        [out:json];node(around:1600,52.516667,13.383333)["amenity"="post_box"];out qt 13;
    """
    TYPE = None
    BASE_URL = 'http://overpass-api.de/api/interpreter'

    def __init__(self):
        self._base_url = Overpass.BASE_URL
        self._radius_in_meters = 1000
        self._limit = None
        self._selection = ''
        self._location = None
        self._sorted = False

    def around(self) -> pd.DataFrame:
        payload = f'{self._out_format};{self._around}{self.selection};{self._out_params};'
        return self.fetch(payload)

    def fetch(self, payload: str) -> pd.DataFrame:
        logging.debug('Requesting overpass data with: %s', payload)
        filepath = CACHE_PATH / f'{md5_hash(payload)}.overpass.pkl'
        if os.path.isfile(filepath):
            logging.debug('Loading overpass response from "%s" as pd.DataFrame!', filepath)
            return pd.read_pickle(filepath)
        else:
            logging.debug('Fetching overpass response!')
            response = requests.get(url=self.url, params={'data': payload}).json()
            frame = pd.json_normalize(response, 'elements')
            logging.debug('Saving overpass response to "%s" as pd.DataFrame!', filepath)
            frame.to_pickle(filepath)
            return frame

    @property
    def url(self) -> str:
        return self._base_url

    @url.setter
    def url(self, value: str) -> None:
        self._base_url = value

    @property
    def location(self) -> Location:
        return self._location

    @location.setter
    def location(self, value: Location) -> None:
        self._location = value

    @property
    def radius(self) -> int:
        return self._radius_in_meters

    @radius.setter
    def radius(self, value: int) -> None:
        self._radius_in_meters = value

    @property
    def limit(self) -> str:
        return f' {self._limit}' if self._limit is not None else ''

    @limit.setter
    def limit(self, value: int) -> None:
        self._limit = f'out qt {value};'

    @property
    def selection(self) -> str:
        return self._selection

    @selection.setter
    def selection(self, value: str) -> None:
        self._selection = value

    @property
    def sorted(self) -> bool:
        return self._sorted

    @sorted.setter
    def sorted(self, value: bool) -> None:
        self._sorted = value

    @property
    def _out_format(self) -> str:
        return '[out:json]'

    @property
    def _out_params(self) -> str:
        sort_param = ' qt' if self.sorted else ''
        return f'out geom{sort_param}{self.limit}'

    @property
    def _around(self) -> str:
        if self.radius is None:
            raise ValueError('Radius not defined yet! Please provide a radius.')
        if self.location is None:
            raise ValueError('Location not defined yet! Please provide a location.')
        return f'{self.TYPE}(around:{self.radius},{self.location.latitude},{self.location.longitude})'
