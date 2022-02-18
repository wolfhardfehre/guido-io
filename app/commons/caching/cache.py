import logging
from pathlib import Path
from typing import Callable, Optional, Any

from app.commons import io
from app.commons.caching.CacheHash import CacheHash
from app.paths import CACHE_PATH


class Cache:

    def __init__(self, func: Callable, *args: Any, **kwargs: Any):
        sub_folder = kwargs.pop('sub_folder', None)
        self.use_cache = kwargs.pop('use_cache', True)
        cache_dir = self._cache_dir(
            cache_dir=kwargs.pop('folder', CACHE_PATH),
            sub_folder=sub_folder
        )
        self._callable = lambda: func(*args, **kwargs)
        cache_hash = CacheHash(args, kwargs, func)
        self._filepath: Path = cache_dir / cache_hash.filename

    def __call__(self) -> Any:
        if self.use_cache and self._filepath.is_file():
            return self._read_cache()
        content = self._content
        if self.use_cache:
            self._write_cache(content)
        return content

    @staticmethod
    def _cache_dir(cache_dir: Path, sub_folder: Optional[str]) -> Path:
        if sub_folder:
            cache_dir = cache_dir / sub_folder
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def _read_cache(self) -> Any:
        logging.debug('Read cache of %s', self._filepath.name)
        return io.read(self._filepath)

    @property
    def _content(self) -> Any:
        return self._callable()

    def _write_cache(self, content: Any) -> None:
        logging.debug('Write cache of %s', self._filepath.name)
        io.write(content=content, filepath=self._filepath)
