import functools

from google.appengine.api import memcache

import malcat

MEMCACHE_TIMEOUT = malcat.config.get('MEMCACHE_TIMEOUT')


def cache_list(get_list):
    @functools.wraps(get_list)
    def get_list_with_cache(username, list_type):
        key = '{}-{}-list'.format(username.lower(), list_type.lower())
        series_list = memcache.get(key)
        if series_list is None:
            # Use list because generators are not pickleable and to prevent
            # the cache from exhausting the iterator
            series_list = list(get_list(username, list_type))
            try:
                memcache.set(key, series_list, time=MEMCACHE_TIMEOUT)
            # Fail silently if the result is too large to store in Memcache.
            except ValueError:
                pass
        return series_list
    return get_list_with_cache


def cache_status_info(get_status_info):
    @functools.wraps(get_status_info)
    def get_status_info_with_cache(username):
        key = '{}-status_info'.format(username.lower())
        status_info = memcache.get(key)
        if status_info is None:
            status_info = get_status_info(username)
            try:
                memcache.set(key, status_info, time=MEMCACHE_TIMEOUT)
            except ValueError:
                pass
        return status_info
    return get_status_info_with_cache
