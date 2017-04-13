import functools
import types

from werkzeug.contrib.cache import GAEMemcachedCache

import malcat


MEMCACHE_TIMEOUT = malcat.config.get('MEMCACHE_TIMEOUT')


class Cache(GAEMemcachedCache):

    def decorate(self, func):
        @functools.wraps(func)
        def get_item(*args, **kwargs):
            if func.__name__ is 'get_list':
                key_suffix = 'list'
            elif func.__name__ is 'get_status_info':
                key_suffix = 'status_info'
            else:
                key_suffix = func.__name__

            key = '-'.join(list(map(lambda arg: str(arg).lower(), args)) + [key_suffix])
            value = self.get(key)
            if value is None:
                value = func(*args, **kwargs)
                # Can't cache generators
                if isinstance(value, types.GeneratorType):
                    value = list(value)

                try:
                    self.set(key, value, MEMCACHE_TIMEOUT)
                except ValueError:
                    # value is too large for memcache
                    pass
            return value
        return get_item


memcache = Cache(None, MEMCACHE_TIMEOUT)
