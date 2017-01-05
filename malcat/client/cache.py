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
            # FIXME: This needs work.
            # If the `user` and `list` parameters aren't present in the URL,
            # the client's browser may cache one response and not update it
            # for other pages. (What's odd is that there's only been one report
            # of this happening, when it should be really be crashing all over
            # the place. :/)
            if not ('user' in flask.request.args and 'list' in flask.request.args):
                # The response was created using the referer header, so it'll change
                # if the referer changes.
                response.headers['Vary'] = 'Referer'
            return response
        return add_cache_headers
    return cache_decorator
