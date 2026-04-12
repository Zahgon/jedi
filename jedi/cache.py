"""
This caching is very important for speed and memory optimizations. There's
nothing really spectacular, just some decorators. The following cache types are
available:

- ``time_cache`` can be used to cache something for just a limited time span,
  which can be useful if there's user interaction and the user cannot react
  faster than a certain time.

This module is one of the reasons why |jedi| is not thread-safe. As you can see
there are global variables, which are holding the cache information. Some of
these variables are being cleaned after every API usage.
"""
import time
from functools import wraps
from typing import Any, Dict, Tuple

from jedi import settings
from parso.cache import parser_cache

_time_caches: Dict[str, Dict[Any, Tuple[float, Any]]] = {}


def clear_time_caches(delete_all: bool = False) -> None:
    """ Jedi caches many things, that should be completed after each completion
    finishes.

    :param delete_all: Deletes also the cache that is normally not deleted,
        like parser cache, which is important for faster parsing.
    """
    pass


def signature_time_cache(time_add_setting):
    """
    This decorator works as follows: Call it with a setting and after that
    use the function with a callable that returns the key.
    But: This function is only called if the key is not available. After a
    certain amount of time (`time_add_setting`) the cache is invalid.

    If the given key is None, the function will not be cached.
    """
    def _temp(key_func):
        pass
    return _temp


def time_cache(seconds):
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            pass

        wrapper.clear_cache = lambda: cache.clear()
        return wrapper

    return decorator


def memoize_method(method):
    """A normal memoize function."""
    pass
