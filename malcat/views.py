import string
from collections import OrderedDict

from flask import Response, request

from malcat import app, cache
from malcat.generators import css_per_series, status_headers
from malcat.constants import (
    status_header_templates,
    output_header
)
from malcat.scrape import get_select_list_nodes
from malcat.request import (
    get_list_arg,
    get_template,
    cacheable_request_url,
    user_is_unknown
)
from malcat.helpers import lxml_to_odict
from malcat.errors import WhoTheHellAreYouError


@app.route('/series')
@cache.cached(900, key_prefix=cacheable_request_url, unless=user_is_unknown)
def series_css_generator():
    username = get_list_arg('user')
    list_type = get_list_arg('list').lower()
    template = get_template()
    user_list = map(lxml_to_odict, get_select_list_nodes(
        username,
        list_type,
        tag=list_type
    ))
    css = css_per_series(user_list, list_type, template)
    header_comments = output_header.format(
        username=username,
        list_type=list_type,
        template=template
    )
    return Response(
        '\n'.join([header_comments, *css]),
        mimetype='text/css'
    )


@app.route('/headers')
@cache.cached(900, key_prefix=cacheable_request_url, unless=user_is_unknown)
def modern_headers_generator():
    username = get_list_arg('user')
    list_type = get_list_arg('list').lower()
    template = ('body[data-query*=\'"status":7\'] .list-item:nth-child({n}) '
                '.data.status:before {{ content: "{content}"; }}')
    header_titles = status_header_templates[list_type]
    for key in header_titles.keys():
        if key in request.args:
            header_titles[key] = request.args[key]
    user_info = map(
        lxml_to_odict,
        get_select_list_nodes(
            username,
            list_type,
            tag='myinfo'
        )
    )
    try:
        totals = OrderedDict(zip(
            header_titles.keys(),
            map(int, list(next(user_info).values())[2:7])
        ))
        print(totals)
    except StopIteration:
        raise WhoTheHellAreYouError(username)
    css = status_headers(header_titles.values(), totals.values(), template)
    return Response('\n'.join(css), mimetype='text/css')


@app.errorhandler(400)
@app.errorhandler(404)
def handle_bad_request(error):
    return Response(
        '/* {} */'.format(error.description),
        mimetype='text/plain'
    )
