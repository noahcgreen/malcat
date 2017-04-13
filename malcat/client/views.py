import functools
import string

import flask

import malcat
from malcat.client import app, request, cache as client_cache
from malcat.server import cssify, scrape
from malcat.server.scrape import cache as server_cache


def css_view(func):
    """Add CSS mimetype to a response."""
    @functools.wraps(func)
    def css_view_func(*args, **kwargs):
        css = func(*args, **kwargs)
        response = flask.make_response(css)
        response.mimetype = 'text/css'
        return response
    return css_view_func


@app.route('/series')
@client_cache.cache(max_age=server_cache.MEMCACHE_TIMEOUT)
@css_view
def series():
    username, list_type = request.list_identifiers()
    template = request.series_template()
    series_list = scrape.get_list(username, list_type)
    css = cssify.template_per_series(
        string.Template(template),
        series_list,
        list_type
    )
    return '\n'.join(css)


@app.route('/headers')
@client_cache.cache(max_age=server_cache.MEMCACHE_TIMEOUT)
@css_view
def headers():
    username, list_type = request.list_identifiers()
    header_contents = request.status_args(list_type)
    template = flask.request.args.get('template', malcat.config['default header css'])
    status_info = scrape.get_status_info(username)[list_type]
    status_mapping = zip(header_contents.values(), status_info)
    css = cssify.template_per_status(string.Template(template), *status_mapping)
    return '\n'.join(css)
