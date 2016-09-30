import functools
import urlparse
from collections import OrderedDict

from flask import request, make_response

import malcat


def package_css(func):
    @functools.wraps(func)
    def css_response(*args, **kwargs):
        css = func(*args, **kwargs)
        response = make_response(css)
        response.mimetype = 'text/css'
        return response
    return css_response


def get_list_identifiers():
    try:
        username = request.args['user']
        list_type = request.args['list']
    except KeyError as e:
        try:
            referer = request.headers['REFERER']
        except KeyError:
            raise e
        else:
            url_path = urlparse.urlparse(referer).path
            username = url_path[11:]
            list_type = url_path[1:6]
    return username, list_type


def get_series_template():
    try:
        template = request.args['template']
    except KeyError as e:
        try:
            preset = request.args['preset']
        except KeyError:
            print('t', type(e))
            raise e
        else:
            template = malcat.CONFIG['series template presets'][preset]
    return template


def get_status_args(list_type):
    statuses = OrderedDict(
        (k, request.args.get(k, v)) for k, v
        in malcat.CONFIG['list types'][list_type.lower()]['statuses']
    )
    return statuses
