import os
import logging
import requests

from app.commons.progress_bar import ProgressBar
from app.config import CACHE_PATH


class Geofabrik:
    BASE_URL = 'https://download.geofabrik.de'
    CHUNK_SIZE = 50 * 1024

    @classmethod
    def fetch(cls, **kwargs):
        address = cls._address(**kwargs)
        url = f'{Geofabrik.BASE_URL}/{"/".join(address)}-latest.osm.pbf'
        file_name = f'{CACHE_PATH}/{"-".join(address)}-latest.osm.pbf'
        if not os.path.isfile(file_name):
            logging.debug(f'fetching data from {url}')
            cls._download(url, file_name)
            logging.debug(f'Saved data in {file_name}')
        else:
            logging.info(f'Pbf file is already in cache: {file_name}')
        return file_name

    @staticmethod
    def _address(**kwargs):
        continent = kwargs.get('continent', None)
        country = kwargs.get('country', None)
        state = kwargs.get('state', None)
        addresses = [continent, country, state]
        return [address for address in addresses if address]

    @staticmethod
    def _file_name(url):
        return f'{CACHE_PATH}/{url.split("/")[-1]}'

    @classmethod
    def _download(cls, url, file_name):
        with requests.get(url, stream=True) as stream:
            stream.raise_for_status()
            cls._write_chunks(file_name, stream)
        return file_name

    @staticmethod
    def _write_chunks(file_name, stream):
        total = int(stream.headers['Content-Length'])
        prefix = f'Downloading [{file_name.split("/")[-1]}]'
        progress_bar = ProgressBar(total=total, prefix=prefix)
        with open(file_name, 'wb') as file:
            for chunk in stream.iter_content(chunk_size=Geofabrik.CHUNK_SIZE):
                file.write(chunk)
                progress_bar.update(len(chunk))


if __name__ == '__main__':
    Geofabrik.fetch(
        continent='europe',
        country='germany',
        state='berlin'
    )
