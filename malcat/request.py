from urllib.parse import urlencode, urlparse

from flask import request

from malcat.errors import MissingArgError
from malcat.constants import series_css_presets


def cacheable_request_url():
    """Return the request url with sorted params for consistent caching."""
    path = request.path
    if not request.args:
        return path.lower()
    params = sorted(request.args.items())
    return (path + '?' + urlencode(params)).lower()


def parse_referer(referer):
    path = urlparse(referer).path
    username = path[11:]
    list_type = path[1:6]
    return { 'user': username, 'list': list_type }


def get_list_arg(param):
    """Get args that can be pulled from the REFERER header."""
    try:
        arg = request.args[param]
    except KeyError as e:
        try:
            arg = parse_referer(request.args['REFERER'])[param]
        except KeyError:
            raise MissingArgError(*e.args)
    return arg


def get_template():
    try:
        return series_css_presets[request.args['preset'].lower()]
    except KeyError:
        try:
            return request.args['template']
        except KeyError:
            raise MissingArgError('template/preset')


def user_is_unknown():
    """Return True if the user cannot be determined."""
    return not any([
        'REFERER' in request.headers,
        'user' in request.args
    ])
