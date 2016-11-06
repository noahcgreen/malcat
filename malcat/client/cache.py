import functools

import flask


def cache(max_age=0):
    def cache_decorator(func):
        @functools.wraps(func)
        def add_cache_headers(*args, **kwargs):
            response = flask.make_response(func(*args, **kwargs))
            response.add_etag()
            response.cache_control.max_age = max_age
            response.make_conditional(flask.request)
            return response
        return add_cache_headers
    return cache_decorator
