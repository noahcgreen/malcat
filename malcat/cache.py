import functools
import cPickle

from flask import make_response, request
from google.appengine.api import memcache


def client_cache(max_age=0):
    def client_cache_decorator(func):
        @functools.wraps(func)
        def add_cache_headers(*args, **kwargs):
            response = make_response(func(*args, **kwargs))
            response.add_etag()
            response.cache_control.max_age = max_age
            response.make_conditional(request)
            print('HEADERS', response.headers)
            return response
        return add_cache_headers
    return client_cache_decorator


class Chunker(object):
    MEMCACHE_MAX_ITEM_SIZE = 900 * 1024

    @classmethod
    def delete(cls, key, *args, **kwargs):
        chunk_keys = memcache.get(key)
        if chunk_keys is None:
            return False
        chunk_keys.append(key)
        return memcache.delete(chunk_keys, *args, **kwargs)

    @classmethod
    def add(cls, key, value, *args, **kwargs):
        if memcache.get(key) is not None:
            return False
        pickled_value = cPickle.dumps(value)
        print(len(pickled_value))
        chunks = {
            key + str(i): pickled_value[pos:pos + cls.MEMCACHE_MAX_ITEM_SIZE]
            for i, pos in enumerate(range(0, len(pickled_value), cls.MEMCACHE_MAX_ITEM_SIZE))
        }
        chunks[key] = chunks.keys()
        return memcache.set_multi(chunks, *args, **kwargs)

    @classmethod
    def get(cls, keys, *args, **kwargs):
        chunks = memcache.get_multi(keys, *args, **kwargs)
        print('KEYS', keys)
        if any(key not in chunks.keys() for key in keys):
            return None
        value = cPickle.loads(''.join(chunks[k] for k in sorted(chunks.keys())))
        print([len(chunk) for chunk in chunks])
        return value


def server_cache(expire=0):
    def server_cache_decorator(func):
        @functools.wraps(func)
        def hit_cache(*args, **kwargs):
            key = str(sorted(args)) + str(sorted(kwargs.items()))
            result = memcache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                try:
                    print('normal')
                    memcache.add(key, result, time=expire)
                except ValueError:
                    print('chunked')
                    Chunker.add(key, result, time=expire)
            elif isinstance(result, list):
                result = Chunker.get(result)
            return result
        return hit_cache
    return server_cache_decorator
