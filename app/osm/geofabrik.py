import logging

import requests

from app.commons.progress_bar import progress_bar
from app.config import CACHE_PATH


class Geofabrik:
    BASE_URL = 'https://download.geofabrik.de'
    CHUNK_SIZE = 50 * 1024

    @classmethod
    def fetch(cls, continent, country=None, state=None):
        url = cls._url(continent, country, state)
        file_name = cls._file_name(url)
        logging.debug(f'fetching data from {url}')
        cls._download(url, file_name)
        logging.debug(f'Saved data in {file_name}')
        return url, file_name

    @classmethod
    def _url(cls, continent, country, state):
        addresses = [continent, country, state]
        addresses = [address for address in addresses if address]
        addresses = '/'.join(addresses)
        return f'{cls.BASE_URL}/{addresses}-latest.osm.pbf'

    @classmethod
    def _file_name(cls, url):
        return f'{CACHE_PATH}/{url.split("/")[-1]}'

    @classmethod
    def _download(cls, url, file_name):
        with requests.get(url, stream=True) as stream:
            stream.raise_for_status()
            cls._write_chunks(file_name, stream)
        return file_name

    @classmethod
    def _write_chunks(cls, file_name, stream):
        total = int(stream.headers['Content-Length'])
        bytes_downloaded = 0
        prefix = f'Downloading [{file_name.split("/")[-1]}]'
        progress_bar(bytes_downloaded, total, prefix=prefix)
        with open(file_name, 'wb') as file:
            for chunk in stream.iter_content(chunk_size=cls.CHUNK_SIZE):
                file.write(chunk)
                bytes_downloaded += len(chunk)
                progress_bar(bytes_downloaded, total, prefix=prefix)


if __name__ == '__main__':
    Geofabrik.fetch(
        continent='europe',
        country='germany',
        state='berlin'
    )
