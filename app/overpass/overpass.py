import requests
import pandas as pd
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

    def around(self):
        payload = f'{self._out_format};{self._around}{self.selection};{self._out_params};'
        return self.fetch(payload)

    def fetch(self, payload) -> pd.DataFrame:
        response = requests.get(url=self.url, params={'data': payload}).json()
        return pd.json_normalize(response, 'elements')

    @property
    def url(self):
        return self._base_url

    @url.setter
    def url(self, value: str):
        self._base_url = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value: Location):
        self._location = value

    @property
    def radius(self):
        return self._radius_in_meters

    @radius.setter
    def radius(self, value: int):
        self._radius_in_meters = value

    @property
    def limit(self):
        return f' {self._limit}' if self._limit is not None else ''

    @limit.setter
    def limit(self, value: int):
        self._limit = f'out qt {value};'

    @property
    def selection(self):
        return self._selection

    @selection.setter
    def selection(self, value: str):
        self._selection = value

    @property
    def sorted(self):
        return self._sorted

    @sorted.setter
    def sorted(self, value: bool):
        self._sorted = value

    @property
    def _out_format(self):
        return '[out:json]'

    @property
    def _out_params(self):
        sort_param = ' qt' if self.sorted else ''
        return f'out geom{sort_param}{self.limit}'

    @property
    def _around(self):
        if self.radius is None:
            raise ValueError('Radius not defined yet! Please provide a radius.')
        if self.location is None:
            raise ValueError('Location not defined yet! Please provide a location.')
        return f'{self.TYPE}(around:{self.radius},{self.location.latitude},{self.location.longitude})'
