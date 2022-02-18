from functools import wraps, partial
from typing import Callable, Optional, Any

from app.commons.caching.cache import Cache


def cache(func: Optional[Callable] = None, **cache_kwargs: Any):
    if func is None:
        return partial(cache, **cache_kwargs)

    @wraps(func)
    def cache_it(*args: Any, **kwargs: Any):
        caching = Cache(func, *args, **cache_kwargs, **kwargs)
        return caching()
    return cache_it
