import logging
from pathlib import Path
from typing import Any, List

import requests
from requests import Response
from tqdm import tqdm

from app.paths import CACHE_PATH


class Geofabrik:
    BASE_URL = 'https://download.geofabrik.de'
    CHUNK_SIZE = 50 * 1024

    @classmethod
    def fetch(cls, **kwargs) -> Path:
        address = cls._address(**kwargs)
        filepath = CACHE_PATH / f'{address[-1]}-latest.osm.pbf'
        if not filepath.exists():
            url = f'{Geofabrik.BASE_URL}/{"/".join(address)}-latest.osm.pbf'
            logging.debug('fetching data from %s', url)
            cls._download(url, filepath)
            logging.debug('Saved data in %s',  filepath)
        else:
            logging.info('Pbf file is already in cache: %s', filepath)
        return filepath

    @staticmethod
    def _address(**kwargs: Any) -> List['str']:
        continent = kwargs.get('continent', None)
        country = kwargs.get('country', None)
        state = kwargs.get('state', None)
        addresses = [continent, country, state]
        return [address for address in addresses if address]

    @classmethod
    def _download(cls, url: str, filepath: Path) -> Path:
        with requests.get(url, stream=True) as stream:
            stream.raise_for_status()
            cls._write_chunks(filepath=filepath, stream=stream)
        return filepath

    @staticmethod
    def _write_chunks(filepath: Path, stream: Response) -> None:
        total = int(stream.headers['Content-Length'])
        prefix = f'Downloading [{filepath.stem}]'
        with tqdm(total=total, desc=prefix) as progress_bar:
            with filepath.open(mode='wb') as file:
                for chunk in stream.iter_content(chunk_size=Geofabrik.CHUNK_SIZE):
                    file.write(chunk)
                    progress_bar.update(len(chunk))


if __name__ == '__main__':
    Geofabrik.fetch(
        continent='europe',
        country='germany',
        state='berlin'
    )
