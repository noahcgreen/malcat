"""The view functions.

The purpose of each view is to discover the necessary arguments,
pass them to a generator, and return the result as CSS; processing
directly within the view should be implicit and as minimal as
possible. The views are not generators; they run generators.
"""

from .app import app, cache
from .generators import css_per_series, status_headers
from .constants import (series_css_presets,
                        status_header_templates,
                        output_header)
from .scrape import list_nodes
from .errors import AppError
from flask import request, Response
from urllib.parse import urlencode, urlparse
from string import Template


def request_url():
    return (request.path
            + urlencode([(k, v) for k, v in sorted(request.args.items())]))


def get_request_args():
    """Return a user's username and list type."""
    try:
        username, list_type = (request.args['user'],
                               request.args['list'].lower())
    except KeyError as e:
        try:
            list_url = request.headers['REFERER']
            url_path = urlparse(list_url).path
            username, list_type = url_path[11:], url_path[1:6]
        except KeyError:
            raise AppError('Missing "{}" argument'.format(e.args[0]))
    return username, list_type


def user_is_uknown():
    return not any(arg in request.args for arg in ['REFERER', 'user'])


@app.route('/series')
@cache.cached(900, key_prefix=request_url, unless=user_is_uknown)
def series_css_generator():
    """Pass arguments to the per-series generator."""
    username, list_type = get_request_args()
    try:
        template = series_css_presets[request.args['preset'].lower()]
    except KeyError:
        try:
            template = request.args['template']
        except KeyError:
            raise AppError('No template or preset provided')
    template = Template(template)
    user_list = list_nodes(username, list_type, target=list_type)
    css = css_per_series(user_list, list_type, template)
    return Response('\n'.join([output_header.format(username=username,
                                                    list_type=list_type,
                                                    template=template.template),
                               *css]),
                    mimetype='text/css')


@app.route('/headers')
def modern_headers_generator():
    """Pass arguments to the status header generator."""
    username, list_type = get_request_args()
    css_header_template = status_header_templates['css']
    headers = [
        request.args.get(k, v)
        for k, v in status_header_templates[list_type].items()
    ]
    try:
        totals = map(int, list(next(list_nodes(username,
                                               list_type,
                                               'myinfo'))
                               .values())[2:7])
    except StopIteration:
        raise AppError('List retrieved was empty. '
                       'Are you using the right username?')
    css = status_headers(zip(headers, totals), css_header_template)
    return Response('\n'.join(css), mimetype='text/css')


@app.errorhandler(AppError)
def handle_app_error(error):
    """Handle generic app-related errors."""
    return Response('Error: {}'.format(error.message), mimetype='text/plain')
